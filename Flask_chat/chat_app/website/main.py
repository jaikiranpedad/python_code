from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

NAME_KEY = "jai"

@app.route("/login"):
    def login():
        render_template("login.html")

@app.route("/logout"):
    def logout():
        session.pop("user", None)
        return redirect(url_for("login"))

@app.route('/') # www.mysite.com/login
@app.route('/home')
def home():
    if NAME_KEY not in sessions:
        return redirect(url_for("login"))

    name = session[NAME_KEY]
    return render_template("index.html")
