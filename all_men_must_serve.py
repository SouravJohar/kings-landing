from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)


@app.route('/')
def home():
    pass


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        okay = False
        email = request.form['email']
        password = request.form['pass']
        '''
        check with databse
        '''
        if email == "johar.sourav97@gmail.com" and password == "wildfire":
            okay = True
        if okay:
            return redirect(url_for('dashboard'))
        else:
            msg = "Invalid credentials!"
            return render_template('login.html', msg=msg)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["pass"]
        repeat_password = request.form["repeat-pass"]
        okay = True
        if password != repeat_password:
            okay = False
            msg = "Passwords do not match!"

        '''push things into db, error checking'''

        if okay:
            return redirect(url_for("dashboard"))
        else:
            return render_template("signup.html", msg=msg)


app.run()
