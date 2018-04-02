from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.utils import secure_filename
from random import *
import sqlite3 as db
import requests
from functools import wraps
import os
import ast
import json
from database.a320 import a320
import pyqrcode
import time
import sys

MASTER_IP = sys.argv[1]
FAKE = sys.argv[2]

app = Flask(__name__)

app.secret_key = "the_debt_is_payed"
app.config['UPLOAD_FOLDER'] = 'static/aadhar'

conn = db.connect('database/kingsbase.db')
c = conn.cursor()

KEY = 'qp9ezhmfH0yRtBmvkJhIPw'


def sendOTP(otp, to, fake=False):
    if not fake:
        URL = 'https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey={}&senderid=TESTIN&channel=1&DCS=0&flashsms=0&number=91{}&text={}&route=13'.format(
            KEY, to, "Your OTP from Kings Landing is " + str(otp) + ". This OTP is valid for 2 minutes only.")
        requests.get(URL)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            if session['logged_in']:
                return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/dashboard")
@login_required
def dashboard():
    user_email = session["user"]
    c.execute("select name from user where email = '{}'".format(user_email))
    name = c.fetchone()[0]
    fname = name.split()[0]
    return render_template("dashboard.html", user=fname)


@app.route('/otp', methods=["GET", "POST"])
def verifylogin():
    t1 = time.time()
    print t1
    if request.method == "GET":
        if FAKE:
            server_otp = 1111
        else:
            server_otp = choice([i for i in range(1000, 10000)])
        session["server_otp"] = server_otp
        c.execute("select ph_no from user where email = '{}'".format(session["temp_email"]))
        user_ph = c.fetchone()[0]
        if not FAKE:
            sendOTP(to=user_ph, otp=server_otp, fake=False)

        return render_template("loginverify.html", mob=user_ph)
    else:
        t2 = time.time()
        print t2
        if t2 - t1 > 2 * 60:
            return render_template("loginverify.html", mob=user_ph, alert="This OTP has expired. Please request a new OTP.")
        client_otp = int(request.form["otp"])
        if client_otp == session["server_otp"]:
            session["logged_in"] = True
            session["user"] = session["temp_email"]
            session["temp_email"] = None
            return redirect(url_for("dashboard"))
        else:
            return render_template("loginverify.html", msg="Invalid OTP")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        okay = False
        email = request.form['email']
        password = request.form['pass']
        c.execute("select email from login where email = '{}'".format(email))
        emails_db = c.fetchall()
        emails_db = [email_db[0] for email_db in emails_db]
        if email in emails_db:
            c.execute("select password from login where email = '{}';".format(email))
            db_pass = c.fetchone()[0]
            if password == db_pass:
                okay = True
            else:
                msg = "Invalid Credentials!"
        else:
            okay = False
            msg = "No such user exists, sign up."
        if okay:
            session["temp_email"] = email
            return redirect(url_for("verifylogin"))
        else:
            return render_template('login.html', msg=msg)


@app.route("/verify", methods=["GET", "POST"])
def verify():
    t1 = time.time()
    print t1
    if request.method == "GET":
        server_otp = choice([i for i in range(1000, 10000)])
        session["server_otp"] = server_otp
        user_ph = session['temp'][1]
        sendOTP(to=user_ph, otp=server_otp, fake=False)
        return render_template("verify.html", mob=session["temp"][1])
    else:
        t2 = time.time()
        print t2
        print t2 - t1
        if t2 - t1 > 2 * 60:
            return render_template("verify.html", mob=session["temp"][1], alert="This OTP has expired. Please request a new OTP.")
        client_otp = int(request.form["otp"])
        if client_otp == session["server_otp"]:
            c.execute("insert into user values (?, ?, ?, ?, ?, ?, ?)",
                      (session["temp"][0], session["temp"][2], "None", "-1", session["temp"][1], "None", "None"))
            c.execute("insert into login values (?, ?)", (session["temp"][2], session["temp"][3]))
            conn.commit()
            session["logged_in"] = True
            session["user"] = session["temp"][2]
            session['temp'] = None
            return redirect(url_for("dashboard"))
        else:
            return render_template("verify.html", msg="Invalid OTP", mob=session["temp"][1])


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["pass"]
        repeat_password = request.form["repeat-pass"]
        okay = True
        if password != repeat_password:
            okay = False
            msg = "Passwords do not match!"
        c.execute("select email from user")
        emails_db = c.fetchall()
        emails_db = [email_db[0] for email_db in emails_db]
        if email in emails_db:
            okay = False
            msg = "Email already exists! Try logging in instead"
        c.execute("select ph_no from user")
        phone_db = c.fetchall()
        phone_db = [int(ph_db[0]) for ph_db in phone_db]
        if int(phone) in phone_db:
            okay = False
            msg = "Phone number is already registered!"
        if okay:
            session["temp"] = [name, phone, email, password]
            return redirect(url_for("verify"))
        else:
            return render_template("signup.html", msg=msg)


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "GET":
        c.execute("select * from user where email = '{}'".format(session["user"]))
        name, email, address, dob, ph_no, state, country = c.fetchone()
        if dob == "-1":
            dob = None
        if state == "None":
            state = None
        if country == "None":
            country = None
        if address == "None":
            address = None
        c.execute("select * from aadhar where email = '{}'".format(session["user"]))
        aadharquery = c.fetchall()
        aadhar = True
        if len(aadharquery) == 0:
            aadhar = None
        return render_template("profile.html", name=name, email=email, phone=ph_no, dob=dob, address=address, country=country, state=state, aadhar=aadhar)
    else:
        return redirect(url_for("editprofile"))


@app.route("/upcoming")
@login_required
def upcoming():
    c.execute("select travel_id, seats_booked, check_in from travel where traveller = '{}'".format(
        session['user']))
    travels = c.fetchall()
    journeys = []
    i = 1
    for travel in travels:
        journey = {}
        travel_id, seats_booked, check_in = travel
        c.execute("select pnr, no_pax, pax_names, no_economy, no_business, no_first, transit_id from journeys where travel_id = {}".format(travel_id))
        pnr, pax, passengers, no_economy, no_business, no_first, transit_id = c.fetchone()
        passengers = passengers.split(",")
        web_checkin_available = False
        st = ""
        if str(check_in) == "0":
            web_checkin_available = True
        if no_economy > 0:
            seat_type = "Economy"
            st = "economy"
        if no_business > 0:
            seat_type = "Business"
            st = "business"
        if no_first > 0:
            seat_type = "First Class"
            st = "fclass"
        c.execute("select * from airplane_transits where transit_id = {}".format(transit_id))
        _, date, from_, to, from_code, to_code, journey_time, from_time, to_time, fnum = c.fetchone()
        journey["pnr"] = pnr
        journey["date"] = date
        journey["pax"] = pax
        journey["no"] = i
        journey["to"] = to
        journey["from"] = from_
        journey["from_code"] = from_code
        journey["to_code"] = to_code
        journey["from_time"] = from_time
        journey["to_time"] = to_time
        journey["journey_time"] = journey_time
        journey["web_checkin_available"] = web_checkin_available
        journey["passengers"] = passengers
        journey["seat_type"] = seat_type
        journey["fnum"] = fnum
        journey["transit_id"] = transit_id
        journey["st"] = st
        journey["travel_id"] = travel_id
        journey["seats_booked_already"] = seats_booked.replace("_", "")
        i += 1
        journeys.append(journey)

    msg = None
    if len(journeys) == 0:
        msg = "No upcoming journeys."
    try:
        ERR = session["ERR"]
    except:
        ERR = False
    return render_template("upcoming.html", journeys=journeys, msg=msg, ERR=ERR)


@app.route('/editprofile', methods=["GET", "POST"])
@login_required
def editprofile():
    # ph_no=0
    if request.method == "GET":
        c.execute("select * from aadhar where email = '{}'".format(session["user"]))
        aadharquery = c.fetchall()
        aadharid = ""
        aadhar = True
        if len(aadharquery) != 0:
            aadharid, email, aa = aadharquery[0]
            aadhar = None
        User = session["user"]
        c.execute("select * from user where email = '{}'".format(User))
        name, email, address, dob, ph_no, state, country = c.fetchone()
        if dob == "-1":
            dob = ""
        if state == "None":
            state = ""
        if country == "None":
            country = ""
        if address == "None":
            address = ""
        return render_template("editprofile.html", aadharid=aadharid, aadhar=aadhar, name=name, email=email, phonenumber=ph_no, dob=dob, address=str(address), country=country, state=state)
    else:
        if request.method == 'POST':
            c.execute("select * from aadhar where email = '{}'".format(session["user"]))
            aadharquery = c.fetchall()
            if(len(aadharquery) == 0):
                if 'file' not in request.files:
                    flash('No Aadhar picture attached')
                    return redirect(request.url)
                file = request.files['file']
                if file.filename == '':
                    flash('No picture attached.')
                    return redirect(request.url)
                if file:
                    user = session["user"][:-4] + ".jpg"
                    filename = secure_filename(session["user"][:-4] + ".jpg")
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    aadharid = request.form["aadharid"]
                    c.execute("insert into aadhar values (?, ?, ?)",
                              (aadharid, session["user"], "yes"))
                    conn.commit()
        User = session["user"]
        name = request.form["name"]
        phone = request.form["phonenumber"]
        # c.execute("select ph_no from user where email = '{}'".format(User))
        # ph_no=c.fetchone()
        # print ph_no
        # print phone
        c.execute("select * from user where email = '{}'".format(User))
        name, email, address, dob, ph_no, state, country = c.fetchone()
        address = request.form["address"]
        dob = request.form["dob"]
        country = request.form["country"]
        state = request.form["state"]
        aadharid = request.form["aadharid"]
        c.execute("update aadhar set aadharid = ? where email = ?", (aadharid, User))
        c.execute("""UPDATE user SET name = ? ,ph_no = ?,address= ?,dob = ? ,state= ?,country= ? WHERE email= ? """,
                  (name, ph_no, address, dob, state, country, User))
        conn.commit()
        if int(phone) != int(ph_no):
            session['phone'] = phone
            return redirect(url_for("changephno"))
        else:
            return redirect(url_for("profile"))


@app.route('/viewaadhar', methods=["GET", "POST"])
@login_required
def viewaadhar():
    if request.method == "GET":
        user = session["user"][:-4]
        filename = secure_filename(session["user"][:-4] + ".jpg")
        imgpath = '../static/aadhar/' + filename
        return render_template('viewaadhar.html', imgpath=imgpath)


@app.route("/bookseats<data>", methods=["GET", "POST"])
@login_required
def book_seats(data):
    payload = ast.literal_eval(data)
    with open("database/transits.json", 'r') as fp:
        transits = json.load(fp)
    seat_type = payload["st"]

    if request.method == "GET":
        c.execute("select * from aadhar where email = '{}'".format(session["user"]))
        query = c.fetchall()
        if len(query) == 0:
            flash("Updation of Aadhar card is mandatory to web check-in")
            return redirect(url_for("editprofile"))
        blocked = transits[str(payload["transit_id"])][seat_type + "_blocked_seats"]
        return render_template("bookseats.html", payload=payload, layout=a320[seat_type], blocked=json.dumps(blocked))

    if request.method == 'POST':
        cost = request.form["cost"]
        seats_booked = request.form["seats"]
        seats_booked_list = seats_booked.split(",")
        ERR = False
        for seat in seats_booked_list:
            if seat not in transits[str(payload["transit_id"])][seat_type + "_blocked_seats"]:
                transits[str(payload["transit_id"])][seat_type + "_blocked_seats"].append(seat)
            else:
                ERR = True
        if not ERR:
            c.execute("update travel set seats_booked = '{}' where travel_id = {}".format(
                seats_booked, payload["travel_id"]))
            c.execute("update travel set check_in = '1' where travel_id = {}".format(
                payload["travel_id"]))
            conn.commit()
            with open("database/transits.json", "w") as f:
                json.dump(transits, f)
            session["cost"] = cost
            session["payload"] = payload
            session["seats_booked_list"] = seats_booked_list
            if str(cost) == "0":
                return redirect(url_for("getpass"))
            else:
                return redirect(url_for("payment"))
        else:
            session["ERR"] = ERR
            return redirect(url_for("upcoming"))


@app.route("/changephno", methods=["GET", "POST"])
@login_required
def changephno():
    if request.method == "GET":
        server_otp = int(random() * 10000)
        session["server_otp"] = server_otp

        user_ph = session['phone']
        print user_ph
        sendOTP(to=user_ph, otp=server_otp)
        return render_template("loginverify.html")
    else:
        client_otp = int(request.form["otp"])
        if client_otp == session["server_otp"]:
            c.execute("""UPDATE user SET ph_no = ? WHERE email= ? """,
                      (session["phone"], session["user"]))
            conn.commit()
            return redirect(url_for("profile"))
        else:
            return render_template("loginverify.html", msg="Invalid OTP")


@app.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    if request.method == "GET":
        return render_template("payment.html", cost=session["cost"])


@app.route("/rollback")
@login_required
def rollback():
    c.execute("update travel set seats_booked = 'None' where travel_id = {}".format(
        session["payload"]["travel_id"]))
    c.execute("update travel set check_in = '0' where travel_id = {}".format(
        session["payload"]["travel_id"]))
    st = session["payload"]["st"]
    with open("database/transits.json", 'r') as fp:
        transits = json.load(fp)
    for seat in session["seats_booked_list"]:
        transits[str(session["payload"]["transit_id"])][st + "_blocked_seats"].remove(seat)
    with open("database/transits.json", "w") as f:
        json.dump(transits, f)
    conn.commit()
    session.pop('payload', None)
    session.pop('seats_booked_list', None)
    session.pop('cost', None)
    return redirect(url_for("upcoming"))


@app.route('/webcheckin', methods=["GET", "POST"])
@login_required
def webcheckin():
    if request.method == "GET":
        return render_template("webcheckin.html")
    else:
        pnr = request.form["pnr"]
        c.execute("select travel_id from travel where traveller = '{}'".format(session["user"]))
        valid_ids = [id[0] for id in c.fetchall()]
        try:
            c.execute(
                "select travel_id, no_pax, pax_names, no_economy, no_business, no_first, transit_id from journeys where pnr = '{}'".format(pnr))
            travel_id, pax, passengers, no_economy, no_business, no_first, transit_id = c.fetchone()
        except:
            return render_template("webcheckin.html", msg="Not a valid PNR!")
        if travel_id not in valid_ids:
            return render_template("webcheckin.html", msg="Not a valid PNR!")
        passengers = passengers.split(",")
        web_checkin_available = False
        c.execute("select seats_booked, check_in from travel where travel_id = '{}'".format(travel_id))
        seats_booked, check_in = c.fetchone()
        st = ""
        if str(check_in) == "0":
            web_checkin_available = True
        if no_economy > 0:
            seat_type = "Economy"
            st = "economy"
        if no_business > 0:
            seat_type = "Business"
            st = "business"
        if no_first > 0:
            seat_type = "First Class"
            st = "fclass"

        journey = {}
        i = 1
        c.execute("select * from airplane_transits where transit_id = {}".format(transit_id))
        _, date, from_, to, from_code, to_code, journey_time, from_time, to_time, fnum = c.fetchone()
        journey["pnr"] = pnr
        journey["date"] = date
        journey["pax"] = pax
        journey["no"] = i
        journey["to"] = to
        journey["from"] = from_
        journey["from_code"] = from_code
        journey["to_code"] = to_code
        journey["from_time"] = from_time
        journey["to_time"] = to_time
        journey["journey_time"] = journey_time
        journey["web_checkin_available"] = web_checkin_available
        journey["passengers"] = passengers
        journey["seat_type"] = seat_type
        journey["fnum"] = fnum
        journey["transit_id"] = transit_id
        journey["st"] = st
        journey["travel_id"] = travel_id
        journey["seats_booked_already"] = seats_booked.replace("_", "")

        if str(check_in) == '1':
            return render_template("viewflightdetails.html", payload=journey)
        else:
            return redirect("/bookseats" + str(journey))


@app.route("/getpass", methods=["GET", "POST"])
@login_required
def getpass():
    ip = "http://{}:5000/view?".format(MASTER_IP)
    journey = session["payload"]
    dict1 = {}
    dict2 = {}
    i = 0
    for name in journey["passengers"]:
        cname = name.replace(" ", "_")
        data = ip + "pnr=" + journey["pnr"] + "&name=" + cname
        qr_name = journey["pnr"] + "-" + cname
        img = pyqrcode.create(data)
        img.png("static/qrcodes/" + qr_name + ".png", scale=8)
        dict1[name] = "../static/qrcodes/" + qr_name + ".png"
        dict2[name] = session["seats_booked_list"][i].replace("_", "")
        i = i + 1
    terminal = [1, 2][int(journey["fnum"][2:]) % 2 == 0]
    gate = ["A1", "B4"][int(journey["fnum"][2:]) % 2 == 0]
    print terminal, gate
    return render_template("bpass.html", journey=journey, dict=dict1, dict2=dict2, gate=gate, terminal=terminal)


@app.route("/viewpass<data>")
@login_required
def view_pass(data):
    journey = ast.literal_eval(data)
    dict1 = {}
    dict2 = {}
    i = 0
    ip = "http://{}:5000/view?".format(MASTER_IP)

    for name in journey["passengers"]:
        cname = name.replace(' ', '_')
        data = ip + "pnr=" + journey["pnr"] + "&name=" + cname
        qr_name = journey["pnr"] + "-" + cname
        img = pyqrcode.create(data)
        img.png("static/qrcodes/" + qr_name + ".png", scale=8)
        dict1[name] = "../static/qrcodes/" + qr_name + ".png"
        dict2[name] = journey["seats_booked_already"].split(",")[i]
        i = i + 1
    terminal = [1, 2][int(journey["fnum"][2:]) % 2 == 0]
    gate = ["A1", "B4"][int(journey["fnum"][2:]) % 2 == 0]
    return render_template("bpass.html", journey=journey, dict=dict1, dict2=dict2, terminal=terminal, gate=gate)


app.run("0.0.0.0")
