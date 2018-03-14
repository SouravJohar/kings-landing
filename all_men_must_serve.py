from flask import Flask, render_template, redirect, url_for, request, session, flash
from random import random
import sqlite3 as db
import requests
from functools import wraps

# TODO


app = Flask(__name__)
app.secret_key = "the_debt_is_payed"


conn = db.connect('database/kingsbase.db')
c = conn.cursor()


def sendOTP(otp, to, fake=False):
    if not fake:
        URL = 'https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey={}&senderid=TESTIN&channel=2&DCS=0&flashsms=0&number=91{}&text={}&route=13'.format(
            KEY, to, "Your OTP from Kings Landing is " + str(otp))
        requests.get(URL)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            # print "poop"
            if session['logged_in']:
                # print "poop indeed"
                return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
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
    if request.method == "GET":
        server_otp = 1111  # int(random() * 10000)
        session["server_otp"] = server_otp
        # print "boooo", session["temp_email"]
        c.execute("select ph_no from user where email = '{}'".format(session["temp_email"]))
        user_ph = c.fetchone()[0]
        sendOTP(to=user_ph, otp=server_otp, fake=True)
        return render_template("loginverify.html", mob=user_ph)
    else:
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
        # print email
        password = request.form['pass']
        c.execute("select email from login where email = '{}'".format(email))
        emails_db = c.fetchall()
        # print emails_db
        emails_db = [email_db[0] for email_db in emails_db]
        if email in emails_db:
            c.execute("select password from login where email = '{}';".format(email))
            db_pass = c.fetchone()[0]
            if password == db_pass:
                okay = True
            else:
                msg = "Invalid Credentials!"
        else:
            # print email
            # print emails_db
            okay = False
            msg = "No such user exists, sign up."
        if okay:
            session["temp_email"] = email
            # print "lololol", session["temp_email"]
            return redirect(url_for("verifylogin"))
        else:
            return render_template('login.html', msg=msg)


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "GET":
        server_otp = int(random() * 10000)
        session["server_otp"] = server_otp
        user_ph = session['temp'][1]
        sendOTP(to=user_ph, otp=server_otp)
        return render_template("verify.html", mob=session["temp"][1])
    else:
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
        return render_template("profile.html", name=name, email=email, phone=ph_no, dob=dob, address=address, country=country, state=state)


@app.route("/upcoming")
@login_required
def upcoming():
    journeys = [
        {
            "pnr": "PXZ33",
            "date": "12-02-2019",
            "pax": 3,
            "no": 1,
            "to": "Jaipur",
            "from": "Trichy",
            "from_time": "2:20",
            "to_time": "4:50",
            "journey_time": "2h 30m",
            "web_checkin_available": True,
            "passengers": ["Mr. Raj", "Mr. Sourav Johar", "Mr. Prakash"],
            "seat_type": "Economy",
            "fnum":"KL213"

        },
        {
            "pnr": "PXZ09",
            "date": "13-02-2019",
            "pax": 3,
            "no": 2,
            "to": "Pune",
            "from": "Trichy",
            "from_time": "2:20",
            "to_time": "4:50",
            "journey_time": "2h 30m",
            "web_checkin_available": False,
            "passengers": ["Mr. Raj", "Mr. Sourav Johar", "Mr. Prakash"],
            "seat_type": "Economy",
            "fnum":"KL013",
            "already_checked_in": True

        }
    ]
    return render_template("upcoming.html", journeys=journeys)


app.run()
