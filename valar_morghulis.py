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
import sys


TERMINAL = int(sys.argv[1])
GATE = sys.argv[2]

print TERMINAL, GATE
conn = db.connect('database/kingsbase.db')
c = conn.cursor()

app = Flask(__name__)


@app.route('/view')
def view():
    pnr = request.args.get('pnr')
    name = request.args.get('name').replace("_", " ")
    allowed = 1
    try:
        c.execute("select transit_id from journeys where pnr = '{}'".format(pnr))
        transit_id = c.fetchone()[0]
        c.execute("select * from airplane_transits where transit_id = '{}'".format(transit_id))
        transit_id, date, from_place, to_place, from_code, to_code, travel_time, departure_time, arrival_time, flight_no = c.fetchone()
        terminal = [1, 2][int(flight_no[2:]) % 2 == 0]
        gate = ["A1", "B4"][int(flight_no[2:]) % 2 == 0]
        if terminal != TERMINAL or gate != GATE:
            allowed = 0
    except:
        allowed = 0
    webbrowser.open("http://127.0.0.1:5000/dashboards?pnr={}&name={}".format(pnr, name))
    return render_template("b.html", flight_no=flight_no, from_place=from_place, to=to_place, name=name, allowed=allowed, terminal=terminal, gate=gate)


@app.route("/dashboards")
def dashboard():
    pnr = request.args.get('pnr')
    name = request.args.get('name').replace("_", " ")
    allowed = 1
    try:
        c.execute("select transit_id from journeys where pnr = '{}'".format(pnr))
        transit_id = c.fetchone()[0]
        c.execute("select * from airplane_transits where transit_id = '{}'".format(transit_id))
        transit_id, date, from_place, to_place, from_code, to_code, travel_time, departure_time, arrival_time, flight_no = c.fetchone()
        terminal = [1, 2][int(flight_no[2:]) % 2 == 0]
        gate = ["A1", "B4"][int(flight_no[2:]) % 2 == 0]
        if terminal != TERMINAL or gate != GATE:
            allowed = 0
    except:
        allowed = 0
    return render_template("b.html", flight_no=flight_no, from_place=from_place, to=to_place, name=name, allowed=allowed, terminal=terminal, gate=gate)


app.run("0.0.0.0")
