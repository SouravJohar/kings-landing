from flask import Flask, render_template, redirect, url_for, request, session, flash
from random import random
import sqlite3 as db

# TODO

# make otp page for log in
# make otp sending module
# database for user info


app = Flask(__name__)
app.secret_key = "the_debt_is_payed"

conn = db.connect('database/kingsbase.db')
c = conn.cursor()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        okay = False
        email = request.form['email']
        password = request.form['pass']
        c.execute("select email from login")
        emails_db = c.fetchall()
        emails_db = [email_db[0] for email_db in emails_db]
        if email in emails_db:
            c.execute("select password from login where email = '{}'".format(email))
            db_pass = c.fetchone()[0]
            if password == db_pass:
                okay = True
            else:
                msg = "Invalid Credentials!"
        else:
            okay = False
            msg = "No such user exists, sign up."
        if okay:
            session["logged_in"] = True
            session["user"] = email
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', msg=msg)


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "GET":
        server_otp = int(random() * 10000)
        session["server_otp"] = server_otp
        '''
        send otp to Phone
        '''
        return render_template("verify.html", otp=server_otp, mob=session["temp"][1])
    else:
        client_otp = int(request.form["otp"])
        if client_otp == session["server_otp"]:
            '''
            push session temp into db, log in user
            '''
            session['temp'] = None
            return redirect(url_for("login"))
        else:
            session['temp'] = None
            return redirect(url_for("signup"))


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

        '''no pushing, just error checking with db'''

        if okay:
            session["temp"] = [name, phone, email, password]
            return redirect(url_for("verify"))
        else:
            return render_template("signup.html", msg=msg)


app.run()
