from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = "jarvis_secret_key_2026"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBqKzJ8X9LmNpQrStUvWxYz1234567890")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

USERS = {"boss": "boss123"}
CHAT_HISTORY = {} # Memory

def jarvis_commands(text):
    text = text.lower()
    if "open youtube" in text:
        return "Opening YouTube for you sir", "https://youtube.com"
    if "weather" in text and "benin" in text:
        return "Checking weather for Benin City sir... It's warm and sunny ☀️", None
    if "time" in text:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%I:%M %p')} sir", None
    return None, None

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        USERS[request.form["username"]] = request.form["password"]
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/chat", methods=["POST"])
def chat():
    if "user" not in session:
        return jsonify({"error": "Not logged in"})
    
    user = session["user"]
    prompt = request.json["prompt"]
    
    # Check commands first
    cmd_response, link = jarvis_commands(prompt)
    if cmd_response:
        return jsonify({"response": cmd_response, "link": link})
    
    # Memory
    if user not in CHAT_HISTORY:
        CHAT_HISTORY[user] = []
    CHAT_HISTORY[user].append({"role": "user", "parts": [prompt]})
    
    try:
        result = model.generate_content(CHAT_HISTORY[user] + [{"role": "user", "parts": ["You are Jarvis from Iron Man. Be helpful, loyal, and a bit witty."] + CHAT_HISTORY[user]}])
        response = result.text
        CHAT_HISTORY[user].append({"role": "model", "parts": [response]})
    except Exception as e:
        response = f"Error: {str(e)}"
    
    return jsonify({"response": response})

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
