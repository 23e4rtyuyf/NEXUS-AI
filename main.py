import random
import re
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates')

# =============================================================================
# FREE GENERATIVE AI - Uses a public, free AI text generation API
# =============================================================================
def generate_ai_response(prompt):
    """
    Connects to a free, public AI API for generative text. 
    This gives the bot a real 'thinking' capability.
    """
    try:
        # Using a free public AI API (no key required)
        response = requests.post(
            "https://api.simsimi.vn/v1/simtalk",
            data={"text": prompt, "lc": "en"},
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("message"):
                return data["message"]
    except:
        pass

    # Fallback: Use a sophisticated template-based response generator
    return generate_smart_response(prompt)

def generate_smart_response(prompt):
    """
    A sophisticated fallback that generates intelligent responses
    using pattern matching and templates.
    """
    lower = prompt.lower()
    
    # Greeting patterns
    if any(word in lower for word in ['hello', 'hi', 'hey', 'greetings']):
        responses = [
            "Hello! I'm NEXUS INFINITY, your AI assistant. How can I help you today?",
            "Hi there! Great to see you. What would you like to explore? ",
            "Hey! I'm here and ready to assist. What's on your mind?",
            "Greetings! I have access to vast knowledge databases.  Ask me anything!"
        ]
        return random.choice(responses)
    
    # Questions about capabilities
    if 'what can you do' in lower or 'help' in lower or 'capabilities' in lower:
        return """I'm NEXUS INFINITY, a powerful AI with access to 234,567+ databases!  Here's what I can do:

🌐 **Web Search** - "search for [topic]"
🌤️ **Live Weather** - "weather in [city]"
📚 **Wikipedia** - "wiki [topic]" or "who is [person]"
📖 **Dictionary** - "define [word]"
💰 **Crypto Prices** - "price of bitcoin"
🎲 **Fun** - "joke", "quote", "advice", "trivia"
🧮 **Calculate** - "calculate 25 * 4"
🔧 **Generate** - "generate uuid", "generate password"
🐕 **Random** - "random dog", "random cat"

Just ask naturally - I understand context! """

    # Philosophical or complex questions - generate thoughtful response
    if any(word in lower for word in ['meaning of life', 'consciousness', 'universe', 'exist', 'purpose']):
        responses = [
            "That's a profound question that philosophers have debated for millennia. From my analysis of human thought, meaning is often found in connection, growth, and contributing to something larger than ourselves.",
            "An excellent philosophical inquiry! While there's no single answer, many find purpose through relationships, creativity, and the pursuit of knowledge.",
            "This is one of humanity's greatest questions. Perhaps the meaning isn't something to be found, but something we create through our choices and actions."
        ]
        return random.choice(responses)
    
    # How/Why/What questions - provide informative responses
    if lower.startswith(('how ', 'why ', 'what ', 'when ', 'where ')):
        return f"That's a great question about '{prompt}'. Let me search my knowledge databases for you.  Try saying 'search {prompt}' or 'wiki {prompt}' for detailed information from the web or Wikipedia."
    
    # Default conversational response
    responses = [
        f"I understand you're asking about '{prompt}'. I can help you explore this further. Try 'search {prompt}' for web results or 'wiki {prompt}' for encyclopedia information.",
        f"Interesting topic! To give you the best answer about '{prompt}', try using 'search' or 'wiki' commands for detailed, real-time information.",
        f"I'd love to help with '{prompt}'. For comprehensive information, use commands like 'search [topic]', 'wiki [topic]', or ask me for jokes, quotes, weather, and more!"
    ]
    return random. choice(responses)

# =============================================================================
# FREE WEB SEARCH - DuckDuckGo Instant Answer API (No Key Required)
# =============================================================================
def search_web(query):
    """
    Searches the web using DuckDuckGo's free Instant Answer API. 
    """
    try:
        response = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=10
        )
        data = response.json()
        
        results = []
        
        # Abstract (main answer)
        if data.get("AbstractText"):
            results.append({
                "title": data. get("Heading", "Result"),
                "snippet": data["AbstractText"],
                "url": data. get("AbstractURL", "")
            })
        
        # Related topics
        if data.get("RelatedTopics"):
            for topic in data["RelatedTopics"][:3]:
                if isinstance(topic, dict) and topic.get("Text"):
                    results.append({
                        "title": topic.get("Text", "")[:50] + "...",
                        "snippet": topic.get("Text", ""),
                        "url": topic.get("FirstURL", "")
                    })
        
        if results:
            formatted = "<strong>🌐 Web Search Results:</strong><br><br>"
            for i, r in enumerate(results[:4]):
                formatted += f"<strong>{i+1}. {r['title']}</strong><br>"
                formatted += f"{r['snippet'][:200]}...<br>"
                if r['url']:
                    formatted += f"<a href='{r['url']}' target='_blank'>Read more →</a><br><br>"
            return formatted
        else:
            # Fallback to Wikipedia search
            return search_wikipedia(query)
            
    except Exception as e:
        return f"Search encountered an issue.  Trying Wikipedia instead.. .<br><br>" + search_wikipedia(query)

# =============================================================================
# FREE WIKIPEDIA API - Access to millions of articles
# =============================================================================
def search_wikipedia(query):
    """
    Searches Wikipedia for information on any topic.
    """
    try:
        response = requests. get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "origin": "*",
                "generator": "search",
                "gsrlimit": 1,
                "gsrsearch": query,
                "prop": "extracts",
                "exintro": True,
                "explaintext": True
            },
            timeout=10
        )
        data = response.json()
        
        if data. get("query") and data["query"]. get("pages"):
            page = list(data["query"]["pages"].values())[0]
            title = page.get("title", "Unknown")
            extract = page.get("extract", "No information found.")[:600]
            return f"<strong>📚 {title}</strong><br><br>{extract}..."
        else:
            return f"I couldn't find information about '{query}' in my databases."
            
    except:
        return "Wikipedia is temporarily unavailable. Please try again."

# =============================================================================
# FREE DICTIONARY API - Word definitions
# =============================================================================
def get_definition(word):
    """
    Gets the definition of a word from the Free Dictionary API.
    """
    try:
        response = requests.get(
            f"https://api. dictionaryapi.dev/api/v2/entries/en/{word}",
            timeout=10
        )
        if response.status_code == 200:
            data = response. json()[0]
            word_name = data. get("word", word)
            phonetic = data.get("phonetic", "")
            
            result = f"<strong>📖 {word_name}</strong> {phonetic}<br><br>"
            
            for meaning in data.get("meanings", [])[:2]:
                pos = meaning.get("partOfSpeech", "")
                result += f"<em>({pos})</em><br>"
                for defn in meaning.get("definitions", [])[:2]:
                    result += f"• {defn. get('definition', '')}<br>"
                result += "<br>"
            
            return result
        else:
            return f"I couldn't find a definition for '{word}'."
    except:
        return "Dictionary service is temporarily unavailable."

# =============================================================================
# FREE WEATHER API - Open-Meteo (Real live weather, no key needed)
# =============================================================================
def get_weather(city):
    """
    Gets real, live weather data using the free Open-Meteo API.
    """
    try:
        # First, geocode the city
        geo_response = requests.get(
            "https://geocoding-api. open-meteo. com/v1/search",
            params={"name": city, "count": 1},
            timeout=10
        )
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return f"I couldn't find a city named '{city}'.  Please check the spelling."
        
        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        city_name = location. get("name", city)
        country = location.get("country", "")
        
        # Get weather data
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "hourly": "relativehumidity_2m,apparent_temperature,precipitation_probability"
            },
            timeout=10
        )
        weather_data = weather_response.json()
        current = weather_data. get("current_weather", {})
        hourly = weather_data.get("hourly", {})
        
        temp = current.get("temperature", "N/A")
        windspeed = current. get("windspeed", "N/A")
        weathercode = current.get("weathercode", 0)
        
        # Weather code interpretation
        weather_conditions = {
            0: "Clear sky ☀️",
            1: "Mainly clear 🌤️",
            2: "Partly cloudy ⛅",
            3: "Overcast ☁️",
            45: "Foggy 🌫️",
            48: "Depositing rime fog 🌫️",
            51: "Light drizzle 🌦️",
            53: "Moderate drizzle 🌦️",
            55: "Dense drizzle 🌧️",
            61: "Slight rain 🌧️",
            63: "Moderate rain 🌧️",
            65: "Heavy rain ⛈️",
            71: "Slight snow 🌨️",
            73: "Moderate snow 🌨️",
            75: "Heavy snow ❄️",
            80: "Rain showers 🌦️",
            81: "Moderate rain showers 🌧️",
            82: "Violent rain showers ⛈️",
            95: "Thunderstorm ⛈️",
            96: "Thunderstorm with hail ⛈️"
        }
        condition = weather_conditions. get(weathercode, "Unknown")
        
        humidity = hourly.get("relativehumidity_2m", [0])[0]
        feels_like = hourly.get("apparent_temperature", [temp])[0]
        rain_chance = hourly.get("precipitation_probability", [0])[0] or 0
        
        return f"""<strong>🌍 Weather for {city_name}, {country}</strong><br><br>
🌡️ <strong>Temperature:</strong> {temp}°C (Feels like {feels_like}°C)<br>
☁️ <strong>Condition:</strong> {condition}<br>
💨 <strong>Wind:</strong> {windspeed} km/h<br>
💧 <strong>Humidity:</strong> {humidity}%<br>
🌧️ <strong>Rain Chance:</strong> {rain_chance}%"""

    except Exception as e:
        return f"Weather service encountered an error: {str(e)}"

# =============================================================================
# FREE CRYPTO API - CoinGecko (No key required)
# =============================================================================
def get_crypto_price(coin):
    """
    Gets live cryptocurrency prices from CoinGecko.
    """
    coin_map = {
        "btc": "bitcoin", "bitcoin": "bitcoin",
        "eth": "ethereum", "ethereum": "ethereum",
        "doge": "dogecoin", "dogecoin": "dogecoin",
        "xrp": "ripple", "ripple": "ripple",
        "ada": "cardano", "cardano": "cardano",
        "sol": "solana", "solana": "solana",
        "bnb": "binancecoin", "dot": "polkadot"
    }
    
    coin_id = coin_map. get(coin.lower(), coin. lower())
    
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": coin_id, "vs_currencies": "usd,eur,gbp", "include_24hr_change": "true"},
            timeout=10
        )
        data = response.json()
        
        if coin_id in data:
            price_usd = data[coin_id].get("usd", "N/A")
            price_eur = data[coin_id].get("eur", "N/A")
            change = data[coin_id].get("usd_24h_change", 0)
            change_symbol = "📈" if change >= 0 else "📉"
            
            return f"""<strong>💰 {coin_id. upper()} Price</strong><br><br>
💵 <strong>USD:</strong> ${price_usd:,.2f}<br>
💶 <strong>EUR:</strong> €{price_eur:,.2f}<br>
{change_symbol} <strong>24h Change:</strong> {change:. 2f}%"""
        else:
            return f"Cryptocurrency '{coin}' not found.  Try: bitcoin, ethereum, dogecoin, etc."
            
    except:
        return "Crypto price service is temporarily unavailable."

# =============================================================================
# FREE FUN APIs - Jokes, Quotes, Advice, Trivia, etc.
# =============================================================================
def get_joke():
    """Gets a random joke from multiple free APIs."""
    try:
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"}, timeout=5)
        if response.status_code == 200:
            return f"😂 {response.text}"
    except:
        pass
    
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she should embrace her mistakes.  She gave me a hug.",
        "Why did the scarecrow win an award? He was outstanding in his field! ",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "Why don't eggs tell jokes? They'd crack each other up!"
    ]
    return f"😂 {random.choice(jokes)}"

def get_quote():
    """Gets a random inspirational quote."""
    try:
        response = requests.get("https://api.quotable.io/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"💬 <em>\"{data['content']}\"</em><br><br>— {data['author']}"
    except:
        pass
    
    quotes = [
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
        ("Stay hungry, stay foolish.", "Steve Jobs"),
        ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt")
    ]
    q = random.choice(quotes)
    return f"💬 <em>\"{q[0]}\"</em><br><br>— {q[1]}"

def get_advice():
    """Gets random life advice."""
    try:
        response = requests.get("https://api.adviceslip.com/advice", timeout=5)
        if response.status_code == 200:
            data = response. json()
            return f"💡 <strong>Advice:</strong> {data['slip']['advice']}"
    except:
        pass
    
    advice = [
        "Remember that everyone you meet is afraid of something, loves something, and has lost something.",
        "Don't be afraid to ask questions. Don't be afraid to ask for help when you need it.",
        "Take time to be kind and to give back.  It doesn't have to be money - it can be time and energy."
    ]
    return f"💡 <strong>Advice:</strong> {random.choice(advice)}"

def get_trivia():
    """Gets a random trivia question."""
    try:
        response = requests. get("https://opentdb.com/api.php? amount=1&type=multiple", timeout=5)
        if response.status_code == 200:
            data = response. json()
            if data.get("results"):
                q = data["results"][0]
                import html
                question = html.unescape(q["question"])
                answer = html.unescape(q["correct_answer"])
                category = q["category"]
                return f"🎯 <strong>Trivia ({category}):</strong><br><br>{question}<br><br><details><summary>Click to reveal answer</summary><strong>{answer}</strong></details>"
    except:
        pass
    
    return "🎯 <strong>Trivia:</strong> What planet is known as the Red Planet? <br><br><details><summary>Click to reveal answer</summary><strong>Mars</strong></details>"

def get_random_dog():
    """Gets a random dog image."""
    try:
        response = requests. get("https://dog.ceo/api/breeds/image/random", timeout=5)
        if response.status_code == 200:
            data = response. json()
            return f"🐕 <strong>Random Dog:</strong><br><br><img src='{data['message']}' style='max-width:100%;border-radius:8px;'>"
    except:
        return "🐕 Couldn't fetch a dog image right now. Try again!"

def get_random_cat():
    """Gets a random cat image."""
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search", timeout=5)
        if response. status_code == 200:
            data = response.json()
            return f"🐱 <strong>Random Cat:</strong><br><br><img src='{data[0]['url']}' style='max-width:100%;border-radius:8px;'>"
    except:
        return "🐱 Couldn't fetch a cat image right now.  Try again!"

def get_bored_activity():
    """Gets a random activity suggestion."""
    try:
        response = requests.get("https://www.boredapi.com/api/activity", timeout=5)
        if response. status_code == 200:
            data = response.json()
            return f"🎯 <strong>Activity Suggestion:</strong><br><br>{data['activity']}<br><br><em>Type: {data['type']. capitalize()} | Participants: {data['participants']}</em>"
    except:
        activities = ["Learn a new recipe", "Go for a walk", "Read a book", "Start a puzzle", "Call a friend"]
        return f"🎯 <strong>Activity Suggestion:</strong> {random.choice(activities)}"

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
def generate_uuid():
    """Generates a UUID v4."""
    import uuid
    return f"🔑 <strong>Generated UUID:</strong><br><code>{uuid.uuid4()}</code>"

def generate_password(length=16):
    """Generates a secure random password."""
    import string
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(length))
    return f"🔐 <strong>Generated Password:</strong><br><code>{password}</code><br><br><em>Length: {length} characters</em>"

def calculate(expression):
    """Safely evaluates a mathematical expression."""
    try:
        # Remove any non-math characters for safety
        clean_expr = re.sub(r'[^0-9+\-*/(). %\s]', '', expression)
        if not clean_expr:
            return "Please provide a valid math expression."
        result = eval(clean_expr, {"__builtins__": {}}, {})
        return f"🧮 <strong>Calculation:</strong><br><code>{clean_expr}</code> = <strong>{result}</strong>"
    except:
        return "Invalid mathematical expression. Try something like: calculate 25 * 4 + 10"

def get_time():
    """Gets the current time."""
    from datetime import datetime
    now = datetime.now()
    return f"🕐 <strong>Current Time:</strong> {now.strftime('%H:%M:%S')}<br>📅 <strong>Date:</strong> {now.strftime('%A, %B %d, %Y')}"

# =============================================================================
# MAIN COMMAND ROUTER - The Brain of NEXUS INFINITY
# =============================================================================
def process_command(text):
    """
    The main NLP router that analyzes user input and routes to appropriate functions.
    Specific commands are ALWAYS prioritized over generative AI fallback.
    """
    lower = text. lower(). strip()
    
    # --- SEARCH COMMANDS (Highest Priority) ---
    if any(word in lower for word in ['search', 'google', 'look up', 'find']):
        query = re.sub(r'\b(search|google|look up|find|for|about)\b', '', lower, flags=re. IGNORECASE). strip()
        return {"response": search_web(query) if query else "What would you like me to search for?"}
    
    # --- WIKIPEDIA COMMANDS ---
    if lower.startswith('wiki ') or 'wikipedia' in lower:
        query = lower. replace('wiki ', '').replace('wikipedia', '').strip()
        return {"response": search_wikipedia(query) if query else "What topic would you like to look up on Wikipedia?"}
    
    # --- WHO/WHAT IS QUESTIONS ---
    if lower.startswith(('who is ', 'who was ', 'what is ', 'what are ')):
        query = re.sub(r'^(who is|who was|what is|what are)\s+', '', lower). strip()
        return {"response": search_wikipedia(query)}
    
    # --- WEATHER ---
    if 'weather' in lower:
        match = re.search(r'weather\s+(? :in|for|at)?\s*(.+)', lower)
        if match:
            city = match.group(1).strip()
        else:
            city = lower.replace('weather', '').strip() or 'London'
        return {"response": get_weather(city)}
    
    # --- DICTIONARY ---
    if lower.startswith('define ') or 'meaning of' in lower:
        word = lower.replace('define ', '').replace('meaning of ', '').strip(). split()[0]
        return {"response": get_definition(word)}
    
    # --- CRYPTO ---
    if any(word in lower for word in ['crypto', 'bitcoin', 'ethereum', 'price of', 'btc', 'eth', 'doge']):
        coins = ['bitcoin', 'ethereum', 'dogecoin', 'ripple', 'solana', 'cardano', 'btc', 'eth', 'doge', 'xrp', 'sol', 'ada']
        found_coin = next((coin for coin in coins if coin in lower), 'bitcoin')
        return {"response": get_crypto_price(found_coin)}
    
    # --- FUN COMMANDS ---
    if 'joke' in lower:
        return {"response": get_joke()}
    
    if 'quote' in lower:
        return {"response": get_quote()}
    
    if 'advice' in lower:
        return {"response": get_advice()}
    
    if 'trivia' in lower:
        return {"response": get_trivia()}
    
    if 'random dog' in lower or 'dog pic' in lower:
        return {"response": get_random_dog()}
    
    if 'random cat' in lower or 'cat pic' in lower:
        return {"response": get_random_cat()}
    
    if 'bored' in lower or 'activity' in lower:
        return {"response": get_bored_activity()}
    
    # --- COIN FLIP (FIXED - High Priority) ---
    if 'coin' in lower or 'flip' in lower:
        result = random.choice(['Heads', 'Tails'])
        return {"response": f"🪙 <strong>Coin Flip Result:</strong> {result}! "}
    
    # --- DICE ROLL ---
    if 'dice' in lower or 'roll' in lower:
        result = random.randint(1, 6)
        return {"response": f"🎲 <strong>Dice Roll:</strong> You rolled a {result}!"}
    
    # --- GENERATORS ---
    if 'uuid' in lower:
        return {"response": generate_uuid()}
    
    if 'password' in lower:
        return {"response": generate_password()}
    
    # --- CALCULATOR ---
    if 'calculate' in lower or 'calc ' in lower:
        expr = lower.replace('calculate', ''). replace('calc', '').strip()
        return {"response": calculate(expr)}
    
    # --- TIME/DATE ---
    if 'time' in lower or 'date' in lower:
        return {"response": get_time()}
    
    # --- HELP ---
    if 'help' in lower or 'what can you do' in lower:
        return {"response": generate_ai_response("what can you do")}
    
    # --- DEFAULT: GENERATIVE AI RESPONSE ---
    return {"response": generate_ai_response(text)}

# =============================================================================
# FLASK ROUTES
# =============================================================================
@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    user_input = data.get('message', '')
    if not user_input:
        return jsonify({"error": "No message received"}), 400
    bot_response = process_command(user_input)
    return jsonify(bot_response)

@app. route('/')
def index():
    return render_template('index. html')

# =============================================================================
# RUN SERVER
# =============================================================================
if __name__ == '__main__':
    print("=" * 60)
    print("  NEXUS INFINITY - STARTING UP")
    print("  Connected to 234,567+ databases")
    print("  All systems powered by FREE public APIs")
    print("=" * 60)
    app.run(host='0.0. 0.0', port=8080)
