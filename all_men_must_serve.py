from flask import Flask, render_template, redirect, url_for, request, session, flash
from random import random
import sqlite3 as db
import requests


# TODO


app = Flask(__name__)
app.secret_key = "the_debt_is_payed"
KEY = 'qp9ezhmfH0yRtBmvkJhIPw'

conn = db.connect('database/kingsbase.db')
c = conn.cursor()


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    if session["logged_in"]:
        return render_template("dashboard.html", msg="Hello, " + session["user"] + "!")
    else:
        return redirect(url_for("login"))


@app.route('/otp', methods=["GET", "POST"])
def verifylogin():
    if request.method == "GET":
        server_otp = int(random() * 10000)
        session["server_otp"] = server_otp
        print "boooo", session["temp_email"]
        c.execute("select ph_no from user where email = '{}'".format(session["temp_email"]))
        user_ph = c.fetchone()[0]
        URL = 'https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey={}&senderid=TESTIN&channel=2&DCS=0&flashsms=0&number=91{}&text={}&route=13'.format(
            KEY, user_ph, "Your OTP from Kings Landing is " + str(server_otp))
        requests.get(URL)
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
            print email
            print emails_db
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


app.run()
