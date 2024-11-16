import nltk
import requests
from nltk.tokenize import word_tokenize

# Download NLTK resources (if not already done)
nltk.download('punkt')

# Predefined intents and responses
intents = {
    "greeting": ["hello", "hi", "hey"],
    "weather": ["weather", "forecast", "temperature"],
    "farewell": ["bye", "goodbye", "see you"],
    "help": ["help", "support", "assist"]
}

responses = {
    "greeting": "Hello! How can I assist you today?",
    "weather": "Please provide your city name to get the weather details.",
    "farewell": "Goodbye! Have a great day!",
    "help": "I can assist you with weather updates or general queries. Just ask!"
}

# Function to classify user intent
def classify_intent(user_input):
    print(f"[DEBUG] User input: {user_input}")  # Debug: Show user input
    tokens = word_tokenize(user_input.lower())
    print(f"[DEBUG] Tokenized input: {tokens}")  # Debug: Show tokenized input
    for intent, keywords in intents.items():
        if any(word in tokens for word in keywords):
            print(f"[DEBUG] Matched intent: {intent}")  # Debug: Matched intent
            return intent
    print("[DEBUG] No matching intent found")  # Debug: No match
    return "unknown"

# Function to fetch weather data
def get_weather(city):
    print(f"[DEBUG] Fetching weather for city: {city}")  # Debug: City name
    api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        print(f"[DEBUG] Weather API response: {data}")  # Debug: API response
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"The temperature in {city} is {temp}°C with {description}."
        else:
            return "Sorry, I couldn't fetch the weather details. Please check the city name."
    except Exception as e:
        print(f"[DEBUG] Error fetching weather data: {e}")  # Debug: Error
        return "Error fetching weather data. Please try again later."

# Main chatbot loop
print("Chatbot: Hi! I'm your assistant. Type 'bye' to exit.")
while True:
    try:
        # Take input from the user
        user_input = input("You: ")
        print(f"[DEBUG] Received input: {user_input}")  # Debug: Confirm input

        # Check for empty input
        if not user_input.strip():
            print("Chatbot: Please type something!")
            continue

        # Check for exit command
        if user_input.lower() in intents["farewell"]:
            print("[DEBUG] User ended the chat")  # Debug: End chat
            print("Chatbot: Goodbye! Have a nice day!")
            break

        # Classify intent and generate response
        intent = classify_intent(user_input)
        if intent == "weather":
            print("Chatbot: " + responses[intent])
            city = input("You: ")  # Ask for city name
            print(f"[DEBUG] Received city input: {city}")  # Debug: City input
            print("Chatbot: " + get_weather(city))
        elif intent in responses:
            print(f"[DEBUG] Responding to intent: {intent}")  # Debug: Response intent
            print("Chatbot: " + responses[intent])
        else:
            print("[DEBUG] Responding with default response")  # Debug: Default response
            print("Chatbot: I'm sorry, I didn't understand that. Can you rephrase?")
    except Exception as e:
        print(f"[DEBUG] Error during input: {e}")  # Debug: Input error
