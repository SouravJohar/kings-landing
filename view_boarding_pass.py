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


conn = db.connect('database/kingsbase.db')
c = conn.cursor()

app = Flask(__name__)

@app.route('/view')
def dashboard():
    pnr = request.args.get('pnr')
    name = request.args.get('name')
    c.execute("select transit_id from journeys where pnr = '{}'".format(pnr))
    transit_id = c.fetchone()[0]
    c.execute("select * from airplane_transits where transit_id = '{}'".format(transit_id))
    transit_id, date, from_place, to_place, from_code, to_code, travel_time, departure_time, arrival_time, flight_no = c.fetchone()
    webbrowser.open('http://127.0.0.1:5000/dashboard?pnr=' + pnr + '&name=' + name, new=0)
    return render_template("thankyou.html")


@app.route("/dashboard")
def dashboard():
    pnr = request.args.get('pnr')
    name = request.args.get('name')
    c.execute("select transit_id from journeys where pnr = '{}'".format(pnr))
    transit_id = c.fetchone()[0]
    c.execute("select * from airplane_transits where transit_id = '{}'".format(transit_id))
    transit_id, date, from_place, to_place, from_code, to_code, travel_time, departure_time, arrival_time, flight_no = c.fetchone()
    return render_template("b.html", flight_no=flight_no, from_place=from_place, to=to_place, name=name)


app.run("0.0.0.0")
