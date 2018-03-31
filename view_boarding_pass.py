from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.utils import secure_filename
from random import random
import sqlite3 as db
import requests
from functools import wraps
import os
import ast
import json
from database.a320 import a320
import pyqrcode
import webbrowser

# TODO
# boarding pass generator backend and frontend

conn = db.connect('database/kingsbase.db')
c = conn.cursor()
app = Flask(__name__)
pnr="SIE98"
name = ""
@app.route('/view')
def dashboard():
    pnr = request.args.get('pnr')
    name = request.args.get('name')
    print name  + " in view "


    # name]re
    # print(pnr)

    # password = request.args.get('password')
    # user_email = session["user"]
    c.execute("select transit_id from journeys where pnr = '{}'".format(pnr))
    transit_id = c.fetchone()[0]
    print transit_id
    c.execute("select * from airplane_transits where transit_id = '{}'".format(transit_id))
    transit_id ,date ,from_place ,to_place ,from_code,to_code,travel_time ,departure_time ,arrival_time ,flight_no=c.fetchone()
    print date , flight_no
    webbrowser.open('http://127.0.0.1:5000/dashboard?pnr='+pnr+'&name='+name, new=0)
    # fname = name.split()[0]
    return render_template("thankyou.html")

# CREATE TABLE airplane_transits
# transit_id ,date ,from_place ,to_place ,from_code,to_code,travel_time ,departure_time ,arrival_time ,flight_no



@app.route("/dashboard")
# @login_required
def dashboard2():
    print "hello"
    # print pnr
    # print name
    pnr = request.args.get('pnr')
    name = request.args.get('name')

    c.execute("select transit_id from journeys where pnr = '{}'".format(pnr))
    transit_id = c.fetchone()[0]
    print transit_id
    c.execute("select * from airplane_transits where transit_id = '{}'".format(transit_id))
    transit_id ,date ,from_place ,to_place ,from_code,to_code,travel_time ,departure_time ,arrival_time ,flight_no=c.fetchone()
    print date , flight_no
    # user_email = session["user"]
    # c.execute("select name from user where email = '{}'".format(user_email))
    # name = c.fetchone()[0]
    # fname = name.split()[0]
    # return render_template("dashboard.html", user="pree")
    return render_template("b.html",flight_no=flight_no, from_place = from_place , to= to_place, name=name)





app.run("0.0.0.0")
