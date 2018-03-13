from flask import Flask, render_template, redirect, url_for, request, session, flash
from random import random
import sqlite3 as db
import requests
from functools import wraps
from werkzeug.utils import secure_filename
import os
# from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
# from flask.uploads import UploadSet, configure_uploads, IMAGES
# TODO


app = Flask(__name__)
app.secret_key = "the_debt_is_payed"
KEY = 'qp9ezhmfH0yRtBmvkJhIPw'

conn = db.connect('database/kingsbase.db')
c = conn.cursor()
# photos = UploadSet('photos', IMAGES)

app.config['UPLOAD_FOLDER'] = 'static/aadhar'
# configure_uploads(app, photos)


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
    try:
        print session["user"]
    except:
        print "fail"
    session.pop('logged_in', None)
    session.pop('user', None)
    # print "after log out", session
    return redirect(url_for('login'))


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", msg="Hello, " + session["user"] + "!")


@app.route('/otp', methods=["GET", "POST"])
def verifylogin():
    if request.method == "GET":
        server_otp = 1111  # int(random() * 10000)
        session["server_otp"] = server_otp
        # print "boooo", session["temp_email"]
        c.execute("select ph_no from user where email = '{}'".format(session["temp_email"]))
        user_ph = c.fetchone()[0]
        URL = 'https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey={}&senderid=TESTIN&channel=2&DCS=0&flashsms=0&number=91{}&text={}&route=13'.format(
            KEY, user_ph, "Your OTP from Kings Landing is " + str(server_otp))
        # requests.get(URL)
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
        print email
        password = request.form['pass']
        c.execute("select email from login where email = '{}'".format(email))
        emails_db = c.fetchall()
        print emails_db
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
            print "lololol", session["temp_email"]
            return redirect(url_for("verifylogin"))
        else:
            return render_template('login.html', msg=msg)


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "GET":
        server_otp = int(random() * 10000)
        session["server_otp"] = server_otp
        URL = 'https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey={}&senderid=TESTIN&channel=2&DCS=0&flashsms=0&number=91{}&text={}&route=13'.format(
            KEY, session['temp'][1], "Your OTP from Kings Landing is " + str(server_otp))
        requests.get(URL)
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
        c.execute("select * from aadhar where email = '{}'".format(session["user"]))
        aadharquery=c.fetchall()
        aadhar="123"
        if len(aadharquery)==0:
            print("NOne aadhar")
            aadhar=None
        else:
            aadhar="123"


        return render_template("profile.html", name=name, email=email, phone=ph_no, dob=dob, address=address, country=country, state=state,aadhar=aadhar)
    else:
        return redirect(url_for("editprofile"))





#BY preetham
#
#
#
#
#
#
@app.route('/editprofile', methods=["GET", "POST"])
@login_required
def editprofile():

    if request.method == "GET":
        c.execute("select * from aadhar where email = '{}'".format(session["user"]))
        aadharquery=c.fetchall()
        aadhar="132"
        aadharid=""
        if(len(aadharquery)!=0):
            aadharid,email,aa=aadharquery[0]
            aadhar=None
        else:
            # aadharid,email,aa=aadharquery
            print("up here jackass")
        User=session["user"]
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
        print address,name, email , dob, state,aadharid

        return render_template("editprofile.html",aadharid=aadharid, aadhar=aadhar,name=name, email=email, phonenumber=ph_no, dob=dob, address=str(address), country=country, state=state)
    else:
        if request.method == 'POST':
        # check if the post request has the file part
            c.execute("select * from aadhar where email = '{}'".format(session["user"]))
            aadharquery=c.fetchall()

            aadhar="132"
            if(len (aadharquery)==0):
                print "here i am "
                if 'file' not in request.files:
                    flash('No Aadhar pic attached')
                    print("no files fucker!")
                    return redirect(request.url)
                file = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    print("no file name fucker")
                    flash('No selected file')
                    return redirect(request.url)
                if file:

                    user=session["user"][:-4]+".jpg"
                    filename = secure_filename(session["user"][:-4]+".jpg")
                    print user
                    print filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    aadharid=request.form["aadharid"]

                    c.execute("insert into aadhar values (?, ?, ?)",
                              ( aadharid, session["user"], "yes"))
                    conn.commit()
            else:
                aadhar=None
        # file=request.files["aadharpic"]
        # bfilename = photos.save(request.files['aadharpic'])
        # filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print(pic )
        print("pic uploaded I guess")
        print "herer"
        User=session["user"]
        name = request.form["name"]
        print str(name) + " name "
        phone = request.form["phonenumber"]
        # email = request.form["email"]
        print str(phone) + " ph "
        # print str(address) + " name "
        address = request.form["address"]
        print str(address) + " ad "
        dob = request.form["dob"]
        print dob
        country = request.form["country"]
        state = request.form["state"]
        print name
        print phone
        # c.execute("update user set  name= '{}'".format(name) , phone= '{}'".format(phone),  address= '{}'".format(address), dob= '{}'".format(dob),state= '{}'".format(state) where email = '{}'".format(session["user"]))
        c.execute("""UPDATE user SET name = ? ,ph_no = ?,address= ?,dob = ? ,state= ?,country= ? WHERE email= ? """,
  (name,phone,address,dob,state,country,User))
        conn.commit()
        print "reached"
        # return render_template("editprofile.html", name=name, email=email, phonenumber=phone, dob=dob, address=address, country=country, state=state)
        return redirect(url_for("profile"))

@app.route('/viewaadhar', methods=["GET", "POST"])
def viewaadhar():
    if request.method == "GET":
        user=session["user"][:-4]
        filename = secure_filename(session["user"][:-4]+".jpg")
        # print user[:-3]
        imgpath='../static/aadhar/'+filename
        print imgpath
        return render_template('viewaadhar.html',imgpath=imgpath)


app.run(host='0.0.0.0')
