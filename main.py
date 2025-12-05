from flask import Flask, request, jsonify, render_template
import random
import json

# Initialize the Flask App (our server)
app = Flask(__name__, static_folder='.', static_url_path='')

# =================================================================
# THE "BRAIN" - This is where all the logic now lives.
# In a real multi-billion dollar app, these functions would connect
# to massive databases, machine learning models, and other services.
# =================================================================

def process_command(text):
    """
    This is the main NLP (Natural Language Processing) router.
    It identifies the user's intent and calls the appropriate function.
    """
    lower = text.lower()
    
    # Prioritize specific commands over general knowledge
    if "weather" in lower:
        city = text.split('in')[-1].strip() or "New York"
        return get_weather(city)
    if "chess" in lower:
        return {"response": "The chess module is rendered client-side for interactivity. Starting a new game!", "widget": "chess"}
    if "joke" in lower:
        return {"response": get_joke()}
    if "fact" in lower:
        return {"response": get_fact()}
    if "code" in lower and "button" in lower:
        return {"response": "Here is the code for a button:", "widget": "code_button"}
    if "uuid" in lower:
        import uuid
        return {"response": f"Generated UUID v4: <code>{uuid.uuid4()}</code>"}
    if "calculate" in lower:
        try:
            expr = text.replace("calculate", "").strip()
            # Basic safe eval
            result = eval(expr, {"__builtins__": None}, {})
            return {"response": f"The result of <code>{expr}</code> is <strong>{result}</strong>."}
        except:
            return {"response": "Sorry, that was an invalid calculation."}

    # If no specific command is found, default to the Knowledge Gateway
    return get_knowledge(text)

def get_weather(city):
    # This simulates a call to a detailed weather API
    temps = {"new york": 22, "london": 18, "tokyo": 26, "sydney": 15}
    temp = temps.get(city.lower(), random.randint(10, 30))
    conditions = ["Clear Skies", "Partly Cloudy", "Overcast", "Light Rain"]
    return {
        "response": f"Fetching weather for <strong>{city.title()}</strong>...",
        "widget": "weather",
        "data": {
            "city": city.title(),
            "temp": temp,
            "condition": random.choice(conditions),
            "humidity": random.randint(40, 90),
            "wind": random.randint(5, 25)
        }
    }

def get_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she should embrace her mistakes. She gave me a hug.",
        "Why did the scarecrow win an award? Because he was outstanding in his field."
    ]
    return random.choice(jokes)

def get_fact():
    facts = [
        "A single cloud can weigh more than a million pounds.",
        "A group of flamingos is called a 'flamboyance'.",
        "The unicorn is the national animal of Scotland."
    ]
    return f"Did you know? {random.choice(facts)}"

def get_knowledge(query):
    # This simulates calling a massive knowledge graph (like Wikipedia)
    return {"response": f"Searching the Omega Knowledge Gateway for '<strong>{query}</strong>'...<br><br>While I can't access a live generative model in this demonstration, a real backend would connect to a service like GPT here to provide a detailed, human-like answer. This architecture makes that possible."}

# =================================================================
# API ENDPOINT - The "door" that the user interface knocks on
# =================================================================
@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({"error": "No message received"}), 400
        
    # Process the input through the "brain"
    bot_response = process_command(user_input)
    
    return jsonify(bot_response)

# =================================================================
# SERVE THE USER INTERFACE - The initial HTML page
# =================================================================
@app.route('/')
def index():
    # This serves the index.html file to the user's browser.
    return render_template('index.html')

# =================================================================
# MAIN EXECUTION - This starts the server
# =================================================================
if __name__ == '__main__':
    print("===================================")
    print("  NEXUS ARCHITECT Server is running.")
    print("  Open http://127.0.0.1:5000 in your browser.")
    print("===================================")
    app.run(port=5000, debug=False)
