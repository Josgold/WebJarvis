from flask import Flask, render_template, request, jsonify, session
import datetime

app = Flask(__name__)
app.secret_key = "jarvis_boss_secret" 

@app.route("/")
def home():
    return render_template("index_v2.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").lower()
    response = ""

    # MEMORY
    if "my name is" in user_input:
        name = user_input.split("my name is")[1].strip()
        session['memory'] = session.get('memory', {})
        session['memory']['name'] = name
        response = f"Got it boss. I'll call you {name} from now on."
    
    elif "what is my name" in user_input:
        name = session.get('memory', {}).get('name', 'Boss')
        response = f"Your name is {name}"

    # TOOLS
    elif "weather" in user_input:
        response = "The weather in Port Harcourt is 28°C, partly cloudy boss."
    elif "news" in user_input:
        response = "Top news: Tech stocks are up today boss."
    elif "time" in user_input:
        response = f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"
    elif "jarvis" in user_input:
        name = session.get('memory', {}).get('name', 'Boss')
        response = f"Yes {name}? I'm listening."
    else:
        response = f"I heard you say: {user_input}. Still learning more commands boss."
    
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
