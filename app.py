from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os, webbrowser

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    text = request.json['text'].lower()
    reply = process_command(text)
    return jsonify({"reply": reply})

def process_command(text):
    # 1. WAKE WORD CHECK
    if "hey jarvis" in text:
        text = text.replace("hey jarvis", "").strip()
        if text == "": return "Yes boss?"
    
    # 2. OPEN APPS COMMANDS
    if "open chrome" in text:
        os.system("start chrome")
        return "Opening Chrome boss"
    elif "open spotify" in text:
        os.system("start spotify")
        return "Opening Spotify"
    elif "open notepad" in text:
        os.system("start notepad")
        return "Opening Notepad"
    
    # OLD COMMANDS
    if "pen cold" in text:
        return "Pen cold activated boss. Systems cooling."
    elif "time" in text:
        return "Current time is " + datetime.now().strftime("%I:%M %p")
    else:
        return f"Copy that boss. You said: {text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)