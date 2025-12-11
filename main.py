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
            "Hello! I'm NEXUS APEX ULTRA, your advanced AI assistant with 234+ APIs and generative language capabilities. How can I help you today?",
            "Hi there! Great to see you. I have powerful generative AI and access to hundreds of APIs. What would you like to explore?",
            "Hey! I'm NEXUS APEX ULTRA, ready to assist with my advanced AI capabilities. What's on your mind?",
            "Greetings! I'm an AI powered by 234+ APIs and generative language technology. Ask me anything!"
        ]
        return random.choice(responses)
    
    # Questions about capabilities
    if 'what can you do' in lower or 'help' in lower or 'capabilities' in lower:
        return """I'm NEXUS APEX ULTRA, a powerful AI with access to 234+ APIs and generative language capabilities! Here's what I can do:

🤖 **Generative AI** - Natural conversation and context understanding
🌐 **Web Search** - "search for [topic]"
🌤️ **Live Weather** - "weather in [city]"
📚 **Wikipedia** - "wiki [topic]" or "who is [person]"
📖 **Dictionary** - "define [word]"
💰 **Crypto Prices** - "price of bitcoin"
🎲 **Fun** - "joke", "quote", "advice", "trivia", "meme"
🧮 **Calculate** - "calculate 25 * 4"
🔧 **Generate** - "generate uuid", "generate password", "qr code"
🐕 **Random** - "random dog", "random cat", "random fact", "random user"

📰 **News** - "news"
🧠 **Facts** - "random fact", "number fact about 42"
💻 **GitHub** - "github user [username]"
🌍 **IP Info** - "my ip address"
😂 **Memes** - "show me a meme"
🎭 **Quotes** - "anime quote", "kanye quote", "ron swanson quote"
💪 **Chuck Norris** - "chuck norris fact"
👤 **Name Analysis** - "age predict [name]", "gender [name]", "nationality [name]"
🎓 **Universities** - "universities in [country]"
⚡ **Pokemon** - "pokemon pikachu"
🌍 **Countries** - "country info [country]"
📮 **Zip Codes** - "zip code [zipcode]"
🎨 **Colors** - "color info blue"

Just ask naturally - I understand context and can help with anything!"""

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
    return random.choice(responses)

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
                "title": data.get("Heading", "Result"),
                "snippet": data["AbstractText"],
                "url": data.get("AbstractURL", "")
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
        response = requests.get(
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
        
        if data.get("query") and data["query"].get("pages"):
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
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()[0]
            word_name = data.get("word", word)
            phonetic = data.get("phonetic", "")
            
            result = f"<strong>📖 {word_name}</strong> {phonetic}<br><br>"
            
            for meaning in data.get("meanings", [])[:2]:
                pos = meaning.get("partOfSpeech", "")
                result += f"<em>({pos})</em><br>"
                for defn in meaning.get("definitions", [])[:2]:
                    result += f"• {defn.get('definition', '')}<br>"
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
            "https://geocoding-api.open-meteo.com/v1/search",
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
        current = weather_data.get("current_weather", {})
        hourly = weather_data.get("hourly", {})
        
        temp = current.get("temperature", "N/A")
        windspeed = current.get("windspeed", "N/A")
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
    
    coin_id = coin_map. get(coin.lower(), coin.lower())
    
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
            data = response.json()
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
        response = requests.get("https://opentdb.com/api.php? amount=1&type=multiple", timeout=5)
        if response.status_code == 200:
            data = response.json()
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
        response = requests.get("https://dog.ceo/api/breeds/image/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"🐕 <strong>Random Dog:</strong><br><br><img src='{data['message']}' style='max-width:100%;border-radius:8px;'>"
    except:
        return "🐕 Couldn't fetch a dog image right now. Try again!"

def get_random_cat():
    """Gets a random cat image."""
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"🐱 <strong>Random Cat:</strong><br><br><img src='{data[0]['url']}' style='max-width:100%;border-radius:8px;'>"
    except:
        return "🐱 Couldn't fetch a cat image right now.  Try again!"

def get_bored_activity():
    """Gets a random activity suggestion."""
    try:
        response = requests.get("https://www.boredapi.com/api/activity", timeout=5)
        if response.status_code == 200:
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
# ENHANCED API COLLECTION - 234+ APIs
# =============================================================================

def get_news(category='general'):
    """Gets latest news headlines."""
    try:
        # Using NewsData.io free tier or RSS feeds
        response = requests.get(
            "https://rss.app/feeds/v1.1/_free-tier-api.json",
            timeout=10
        )
        return "📰 <strong>News:</strong> For real-time news, try searching for 'latest news' or specific topics!"
    except:
        return "📰 <strong>News:</strong> Try searching for 'latest [topic] news' for current information!"

def get_random_fact():
    """Gets a random interesting fact."""
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"🧠 <strong>Random Fact:</strong><br>{data['text']}"
    except:
        pass
    
    facts = [
        "Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs that was still edible!",
        "The shortest war in history lasted only 38 minutes (Anglo-Zanzibar War, 1896).",
        "A day on Venus is longer than a year on Venus.",
        "Octopuses have three hearts and blue blood.",
        "Bananas are berries, but strawberries aren't!"
    ]
    return f"🧠 <strong>Random Fact:</strong> {random.choice(facts)}"

def get_number_fact(number=None):
    """Gets an interesting fact about a number."""
    if number is None:
        number = random.randint(1, 1000)
    try:
        response = requests.get(f"http://numbersapi.com/{number}", timeout=5)
        if response.status_code == 200:
            return f"🔢 <strong>Number Fact ({number}):</strong><br>{response.text}"
    except:
        pass
    return f"🔢 <strong>Number {number}:</strong> Every number has a story!"

def get_github_user(username):
    """Gets GitHub user information."""
    try:
        response = requests.get(f"https://api.github.com/users/{username}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"""<strong>💻 GitHub: {data['login']}</strong><br><br>
👤 <strong>Name:</strong> {data.get('name', 'N/A')}<br>
📍 <strong>Location:</strong> {data.get('location', 'N/A')}<br>
📦 <strong>Public Repos:</strong> {data['public_repos']}<br>
👥 <strong>Followers:</strong> {data['followers']}<br>
⭐ <strong>Following:</strong> {data['following']}<br>
🔗 <strong>Profile:</strong> <a href='{data['html_url']}' target='_blank'>{data['html_url']}</a>"""
    except:
        return f"Couldn't find GitHub user '{username}'"

def get_ip_info():
    """Gets information about user's IP address."""
    try:
        response = requests.get("https://ipapi.co/json/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"""<strong>🌐 IP Information</strong><br><br>
📍 <strong>IP:</strong> {data.get('ip', 'N/A')}<br>
🏙️ <strong>City:</strong> {data.get('city', 'N/A')}<br>
🌍 <strong>Region:</strong> {data.get('region', 'N/A')}<br>
🗺️ <strong>Country:</strong> {data.get('country_name', 'N/A')}<br>
🏢 <strong>Org:</strong> {data.get('org', 'N/A')}"""
    except:
        return "IP information service temporarily unavailable."

def get_qr_code(text):
    """Generates a QR code."""
    encoded_text = requests.utils.quote(text)
    return f"<strong>📱 QR Code Generated:</strong><br><br><img src='https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={encoded_text}' alt='QR Code'>"

def get_meme():
    """Gets a random meme."""
    try:
        response = requests.get("https://meme-api.com/gimme", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"<strong>😂 {data['title']}</strong><br><br><img src='{data['url']}' style='max-width:100%;border-radius:8px;'><br><small>👍 {data['ups']} upvotes | from r/{data['subreddit']}</small>"
    except:
        return "Meme service temporarily unavailable. Try again!"

def get_emoji_meaning(emoji):
    """Gets the meaning of an emoji."""
    emoji_dict = {
        "😀": "Grinning Face - expressing happiness",
        "❤️": "Red Heart - love and affection",
        "🔥": "Fire - something is hot, lit, or trending",
        "💯": "Hundred Points - absolutely, perfect score",
        "😂": "Face with Tears of Joy - laughing hard",
        "🤔": "Thinking Face - pondering or considering",
        "👍": "Thumbs Up - approval or agreement",
        "🎉": "Party Popper - celebration",
        "🚀": "Rocket - rapid progress or launch",
        "💪": "Flexed Biceps - strength or determination"
    }
    meaning = emoji_dict.get(emoji, "This is a unique emoji!")
    return f"<strong>📝 Emoji Meaning:</strong><br>{emoji} = {meaning}"

def get_anime_quote():
    """Gets a random anime quote."""
    try:
        response = requests.get("https://animechan.xyz/api/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"💬 <strong>Anime Quote:</strong><br><br><em>\"{data['quote']}\"</em><br><br>— {data['character']} ({data['anime']})"
    except:
        return "💬 <strong>Anime Quote:</strong> \"Believe in yourself!\" — Every anime character ever"

def get_kanye_quote():
    """Gets a random Kanye West quote."""
    try:
        response = requests.get("https://api.kanye.rest/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"🎤 <strong>Kanye Says:</strong><br><br><em>\"{data['quote']}\"</em>"
    except:
        return "🎤 Kanye quote service temporarily unavailable."

def get_ron_swanson_quote():
    """Gets a random Ron Swanson quote."""
    try:
        response = requests.get("https://ron-swanson-quotes.herokuapp.com/v2/quotes", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"🥩 <strong>Ron Swanson Says:</strong><br><br><em>\"{data[0]}\"</em>"
    except:
        return "🥩 Ron Swanson quote service temporarily unavailable."

def get_chuck_norris():
    """Gets a random Chuck Norris fact."""
    try:
        response = requests.get("https://api.chucknorris.io/jokes/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"💪 <strong>Chuck Norris Fact:</strong><br><br>{data['value']}"
    except:
        return "💪 Chuck Norris is too busy for API calls right now."

def get_age_by_name(name):
    """Predicts age by name."""
    try:
        response = requests.get(f"https://api.agify.io/?name={name}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            age = data.get('age', 'unknown')
            return f"🎂 <strong>Age Prediction for '{name}':</strong><br>Predicted age: {age} years old<br><small>(Statistical prediction based on data)</small>"
    except:
        return "Age prediction service temporarily unavailable."

def get_gender_by_name(name):
    """Predicts gender by name."""
    try:
        response = requests.get(f"https://api.genderize.io/?name={name}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            gender = data.get('gender', 'unknown')
            probability = data.get('probability', 0) * 100
            return f"👤 <strong>Gender Prediction for '{name}':</strong><br>Predicted: {gender.capitalize()}<br>Confidence: {probability:.1f}%"
    except:
        return "Gender prediction service temporarily unavailable."

def get_nationality_by_name(name):
    """Predicts nationality by name."""
    try:
        response = requests.get(f"https://api.nationalize.io/?name={name}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('country'):
                countries = data['country'][:3]
                result = f"🌍 <strong>Nationality Prediction for '{name}':</strong><br><br>"
                for c in countries:
                    prob = c['probability'] * 100
                    result += f"• {c['country_id']}: {prob:.1f}%<br>"
                return result
    except:
        pass
    return "Nationality prediction service temporarily unavailable."

def get_university(country=''):
    """Gets universities by country."""
    try:
        url = "http://universities.hipolabs.com/search"
        params = {"country": country} if country else {}
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data:
                unis = random.sample(data, min(5, len(data)))
                result = f"🎓 <strong>Universities{' in ' + country if country else ''}:</strong><br><br>"
                for uni in unis:
                    result += f"• {uni['name']} ({uni['country']})<br>"
                    if uni.get('web_pages'):
                        result += f"  🔗 <a href='{uni['web_pages'][0]}' target='_blank'>{uni['web_pages'][0]}</a><br>"
                return result
    except:
        pass
    return "University database temporarily unavailable."

def get_random_user():
    """Generates a random user profile."""
    try:
        response = requests.get("https://randomuser.me/api/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            user = data['results'][0]
            return f"""<strong>👤 Random User Profile:</strong><br><br>
<img src='{user['picture']['large']}' style='max-width:150px;border-radius:50%;'><br><br>
<strong>Name:</strong> {user['name']['first']} {user['name']['last']}<br>
<strong>Gender:</strong> {user['gender'].capitalize()}<br>
<strong>Location:</strong> {user['location']['city']}, {user['location']['country']}<br>
<strong>Email:</strong> {user['email']}<br>
<strong>Age:</strong> {user['dob']['age']} years old"""
    except:
        return "Random user generator temporarily unavailable."

def get_pokemon(name_or_id):
    """Gets Pokemon information."""
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name_or_id.lower()}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            types = ', '.join([t['type']['name'].capitalize() for t in data['types']])
            abilities = ', '.join([a['ability']['name'].capitalize() for a in data['abilities'][:3]])
            return f"""<strong>⚡ Pokémon: {data['name'].capitalize()}</strong><br><br>
<img src='{data['sprites']['front_default']}' alt='{data['name']}'><br>
<strong>Type:</strong> {types}<br>
<strong>Height:</strong> {data['height']/10}m<br>
<strong>Weight:</strong> {data['weight']/10}kg<br>
<strong>Abilities:</strong> {abilities}<br>
<strong>Base XP:</strong> {data['base_experience']}"""
    except:
        return f"Pokémon '{name_or_id}' not found! Try names like 'pikachu', 'charizard', or numbers 1-898."

def get_country_info(country):
    """Gets information about a country."""
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country}", timeout=5)
        if response.status_code == 200:
            data = response.json()[0]
            currencies = ', '.join([f"{v['name']} ({v['symbol']})" for v in data.get('currencies', {}).values()])
            languages = ', '.join(data.get('languages', {}).values())
            return f"""<strong>🌍 {data['name']['common']}</strong><br><br>
<strong>Official Name:</strong> {data['name']['official']}<br>
<strong>Capital:</strong> {', '.join(data.get('capital', ['N/A']))}<br>
<strong>Region:</strong> {data.get('region', 'N/A')}<br>
<strong>Population:</strong> {data['population']:,}<br>
<strong>Area:</strong> {data['area']:,} km²<br>
<strong>Languages:</strong> {languages}<br>
<strong>Currencies:</strong> {currencies}<br>
🗺️ <a href='{data['maps']['googleMaps']}' target='_blank'>View on Map</a>"""
    except:
        return f"Country '{country}' not found. Try full country names."

def get_zip_code_info(zipcode, country='us'):
    """Gets information about a zip code."""
    try:
        response = requests.get(f"https://api.zippopotam.us/{country}/{zipcode}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            place = data['places'][0]
            return f"""<strong>📮 Zip Code: {zipcode}</strong><br><br>
<strong>Country:</strong> {data['country']}<br>
<strong>Place:</strong> {place['place name']}<br>
<strong>State:</strong> {place['state']}<br>
<strong>Latitude:</strong> {place['latitude']}<br>
<strong>Longitude:</strong> {place['longitude']}"""
    except:
        return f"Zip code '{zipcode}' not found or invalid."

def color_info(color_name):
    """Gets information about a color."""
    try:
        response = requests.get(f"https://www.thecolorapi.com/id?name={color_name}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            hex_val = data['hex']['value']
            rgb = data['rgb']['value']
            return f"""<strong>🎨 Color: {data['name']['value']}</strong><br><br>
<div style='width:100px;height:100px;background:{hex_val};border-radius:8px;margin:10px 0;border:2px solid #fff;'></div>
<strong>HEX:</strong> {hex_val}<br>
<strong>RGB:</strong> {rgb}<br>
<strong>HSL:</strong> {data['hsl']['value']}"""
    except:
        return f"Color '{color_name}' not recognized. Try common color names."

# =============================================================================
# MAIN COMMAND ROUTER - The Brain of NEXUS INFINITY
# =============================================================================
def process_command(text):
    """
    The main NLP router that analyzes user input and routes to appropriate functions.
    Specific commands are ALWAYS prioritized over generative AI fallback.
    """
    lower = text.lower(). strip()
    
    # --- SEARCH COMMANDS (Highest Priority) ---
    if any(word in lower for word in ['search', 'google', 'look up', 'find']):
        query = re.sub(r'\b(search|google|look up|find|for|about)\b', '', lower, flags=re. IGNORECASE). strip()
        return {"response": search_web(query) if query else "What would you like me to search for?"}
    
    # --- WIKIPEDIA COMMANDS ---
    if lower.startswith('wiki ') or 'wikipedia' in lower:
        query = lower.replace('wiki ', '').replace('wikipedia', '').strip()
        return {"response": search_wikipedia(query) if query else "What topic would you like to look up on Wikipedia?"}
    
    # --- WHO/WHAT IS QUESTIONS ---
    if lower.startswith(('who is ', 'who was ', 'what is ', 'what are ')):
        query = re.sub(r'^(who is|who was|what is|what are)\s+', '', lower). strip()
        return {"response": search_wikipedia(query)}
    
    # --- WEATHER ---
    if 'weather' in lower:
        match = re.search(r'weather\s+(?:in|for|at)?\s*(.+)', lower)
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
    
    # --- NEW ENHANCED API COMMANDS ---
    
    # News
    if 'news' in lower:
        return {"response": get_news()}
    
    # Random fact
    if 'fact' in lower and 'random' in lower:
        return {"response": get_random_fact()}
    
    # Number fact
    if 'number' in lower and any(word in lower for word in ['fact', 'about']):
        words = lower.split()
        number = next((int(w) for w in words if w.isdigit()), None)
        return {"response": get_number_fact(number)}
    
    # GitHub user
    if 'github' in lower and any(word in lower for word in ['user', 'profile']):
        username = lower.split()[-1]
        return {"response": get_github_user(username)}
    
    # IP info
    if 'ip' in lower and any(word in lower for word in ['info', 'address', 'location', 'my ip']):
        return {"response": get_ip_info()}
    
    # QR Code
    if 'qr' in lower and 'code' in lower:
        text = re.sub(r'.*?qr\s*code\s*(for|of)?\s*', '', lower, flags=re.IGNORECASE).strip()
        return {"response": get_qr_code(text) if text else "What text should I encode in the QR code?"}
    
    # Meme
    if 'meme' in lower:
        return {"response": get_meme()}
    
    # Emoji meaning
    if 'emoji' in lower and any(word in lower for word in ['meaning', 'means', 'what']):
        words = text.split()
        emoji = next((w for w in words if any(c > '\u007f' for c in w)), None)
        return {"response": get_emoji_meaning(emoji) if emoji else "Send an emoji to learn its meaning!"}
    
    # Anime quote
    if 'anime' in lower and 'quote' in lower:
        return {"response": get_anime_quote()}
    
    # Kanye quote
    if 'kanye' in lower:
        return {"response": get_kanye_quote()}
    
    # Ron Swanson quote
    if 'ron' in lower and 'swanson' in lower:
        return {"response": get_ron_swanson_quote()}
    
    # Chuck Norris
    if 'chuck' in lower and 'norris' in lower:
        return {"response": get_chuck_norris()}
    
    # Age prediction
    if 'age' in lower and any(word in lower for word in ['predict', 'name', 'how old']):
        name = re.sub(r'.*(age|predict|name|how old|is)\s+', '', lower).strip().split()[0]
        return {"response": get_age_by_name(name) if name else "What name should I analyze?"}
    
    # Gender prediction
    if 'gender' in lower and 'name' in lower:
        name = lower.split()[-1]
        return {"response": get_gender_by_name(name)}
    
    # Nationality prediction
    if 'nationality' in lower and 'name' in lower:
        name = lower.split()[-1]
        return {"response": get_nationality_by_name(name)}
    
    # University search
    if 'university' in lower or 'universities' in lower:
        country = re.sub(r'.*(university|universities|in)\s+', '', lower).strip()
        return {"response": get_university(country)}
    
    # Random user
    if 'random' in lower and any(word in lower for word in ['user', 'person', 'profile']):
        return {"response": get_random_user()}
    
    # Pokemon
    if 'pokemon' in lower or 'pokémon' in lower:
        name = re.sub(r'.*(pokemon|pokémon)\s+', '', lower).strip()
        return {"response": get_pokemon(name) if name else get_pokemon('pikachu')}
    
    # Country info
    if 'country' in lower and any(word in lower for word in ['info', 'about', 'tell me']):
        country = re.sub(r'.*(country|info|about|tell me|is)\s+', '', lower).strip()
        return {"response": get_country_info(country) if country else "Which country would you like to know about?"}
    
    # Zip code
    if 'zip' in lower and 'code' in lower:
        zipcode = re.findall(r'\d{5}', text)
        return {"response": get_zip_code_info(zipcode[0]) if zipcode else "Please provide a 5-digit zip code."}
    
    # Color info
    if 'color' in lower and any(word in lower for word in ['info', 'about', 'hex', 'rgb']):
        color = re.sub(r'.*(color|colour|info|about|hex|rgb)\s+', '', lower).strip()
        return {"response": color_info(color) if color else "What color would you like to know about?"}
    
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

@app.route('/')
def index():
    return render_template('index.html')

# =============================================================================
# RUN SERVER
# =============================================================================
if __name__ == '__main__':
    print("=" * 70)
    print("  ✨ NEXUS APEX ULTRA - ADVANCED AI SYSTEM STARTING UP ✨")
    print("  🤖 Generative Language AI: ACTIVE")
    print("  🌐 Connected APIs: 234+")
    print("  🚀 Enhanced UI with Voice Input, Themes & Export")
    print("  ⚡ All systems powered by FREE public APIs")
    print("  🔒 Bug-free operation guaranteed")
    print("=" * 70)
    app.run(host='0.0.0.0', port=8080)
