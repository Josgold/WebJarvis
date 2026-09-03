from flask import Flask, render_template, request, jsonify
import os
import webbrowser

app = Flask(__name__)

# Your Jarvis logic here
def get_jarvis_response(user_input):
    user_input = user_input.lower()
    
    if "hello" in user_input or "hi" in user_input:
        return "Hello boss, how can I help you today?"
    elif "time" in user_input:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        return f"The current time is {now}"
    elif "open youtube" in user_input:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube for you boss"
    else:
        return f"I heard you say: {user_input}"

# NEW SPEAK FUNCTION - Tells browser to speak instead of server
def speak(text):
    return {"type": "speak", "text": text}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Get Jarvis response
    jarvis_text = get_jarvis_response(user_message)
    
    # Return both text and speak command
    response = speak(jarvis_text)
    response["reply"] = jarvis_text
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)