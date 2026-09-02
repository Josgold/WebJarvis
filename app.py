from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = "jarvis_secret_key_2026"

# Configure Gemini
GEMINI_API_KEY = "AIzaSyBqKzJ8X9LmNpQrStUvWxYz1234567890" # REPLACE WITH YOUR KEY
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Fake users for now
USERS = {
    "boss": "boss123"
}

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        USERS[username] = password
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    
    response = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            result = model.generate_content("You are Jarvis, a helpful AI assistant. " + prompt)
            response = result.text
        except Exception as e:
            response = f"Error: {str(e)}"
    
    return render_template("dashboard.html", user=session["user"], response=response)

@app.route("/auth", methods=["POST"])
def auth():
    username = request.form["username"]
    password = request.form["password"]
    if username in USERS and USERS[username] == password:
        session["user"] = username
        return redirect(url_for("dashboard"))
    return "Wrong password. <a href='/'>Try again</a>"

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
