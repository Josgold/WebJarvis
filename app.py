from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
import webbrowser
import requests
import os

app = Flask(__name__)
app.secret_key = "jarvis_secret_key_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default="user") # user, cohost, host

with app.app_context():
    db.create_all()
    # Create host account if it doesn't exist
    if not User.query.filter_by(username="boss").first():
        host = User(username="boss", password="boss123", role="host")
        db.add(host)
        db.commit()

@app.route("/")
def home():
    if not session.get("user_id"):
        return render_template("login.html")
    if session.get("role") == "host":
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            return "Username already exists! <a href='/signup'>Try again</a>"
        new_user = User(username=username, password=password, role="user")
        db.add(new_user)
        db.commit()
        return redirect(url_for("home"))
    return render_template("signup.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role
        return redirect(url_for("home"))
    return "Wrong login! <a href='/'>Try again</a>"

@app.route("/dashboard")
def dashboard():
    if session.get("role") not in ["host", "cohost"]:
        return "Access denied"
    users = User.query.all()
    return render_template("dashboard.html", users=users)

@app.route("/promote/<int:user_id>")
def promote(user_id):
    if session.get("role") != "host":
        return "Access denied. Only Host can promote"
    user = User.query.get(user_id)
    if user and user.role == "user":
        user.role = "cohost"
        db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/demote/<int:user_id>")
def demote(user_id):
    if session.get("role") != "host":
        return "Access denied. Only Host can demote"
    user = User.query.get(user_id)
    if user and user.role == "cohost":
        user.role = "user"
        db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/command/<cmd>")
def command(cmd):
    if not session.get("user_id"):
        return jsonify({"reply": "Please login first"})
    
    cmd = cmd.lower()
    if "time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return jsonify({"reply": f"The time is {now}"})
    elif "date" in cmd:
        today = datetime.date.today().strftime("%B %d, %Y")
        return jsonify({"reply": f"Today is {today}"})
    elif "weather" in cmd:
        city = "Cotonou, Benin"
        if "in" in cmd:
            city = cmd.split("in")[-1].strip()
        url = f"https://wttr.in/{city}?format=3"
        weather = requests.get(url).text
        return jsonify({"reply": f"Weather in {city}: {weather}"})
    else:
        return jsonify({"reply": "Sorry boss, I didn't get that"})

if __name__ == "__main__":
    app.run(debug=True)
