from flask import Flask, render_template, request, jsonify, session
import requests
import speech_recognition as sr
import pyttsx3
import datetime
import os

app = Flask(__name__)
app.secret_key = "jarvis_boss_secret" # for memory

# TTS setup
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# MEMORY - remembers stuff in this session
if 'memory' not in session:
    session['memory'] = {}

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_weather(city="Port Harcourt"):
    # You can add real API key later. This is demo
    return f"The weather in {city} is 28°C, partly cloudy boss."

def get_news():
    return "Top news: Tech stocks are up today boss."

@app.route("/")
def home():
    return render_template("index_v2.html") # new html

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").lower()
    response = ""

    # MEMORY
    if "my name is" in user_input:
        name = user_input.split("my name is")[1].strip()
        session['memory']['name'] = name
        response = f"Got it boss. I'll call you {name} from now on."
    
    elif "what is my name" in user_input:
        response = f"Your name is {session['memory'].get('name', 'Boss')}"

    # VOICE COMMANDS
    elif "weather" in user_input:
        response = get_weather()
    elif "news" in user_input:
        response = get_news()
    elif "time" in user_input:
        response = f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"
    elif "jarvis" in user_input:
        response = f"Yes {session['memory'].get('name', 'Boss')}? I'm listening."
    else:
        response = f"I heard you say: {user_input}. Still learning more commands boss."
    
    # speak it out
    # speak(response) # Uncomment when testing on PC with speaker
    
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
