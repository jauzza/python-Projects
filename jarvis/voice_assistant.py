import requests
import speech_recognition as sr
import random
import json
import sys

# Google Cloud Natural Language API key
api_key = 'YOUR_API_KEY_HERE'

# File to store responses
responses_file = "responses.json"

# Load responses from file
try:
    with open(responses_file, "r") as file:
        responses = json.load(file)
except FileNotFoundError:
    responses = {}

# Function to save responses to file
def save_responses():
    with open(responses_file, "w") as file:
        json.dump(responses, file)

# Function to transcribe speech to text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        if text.lower() == "jarvis mute":
            print("Jarvis is now muted.")
            return None
        elif text.lower() == "jarvis end":
            print("Ending conversation. Goodbye!")
            sys.exit()
        else:
            return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None

# Analyze sentiment of the transcribed text and generate a response
def analyze_sentiment(text):
    url = 'https://language.googleapis.com/v1/documents:analyzeSentiment?key=' + api_key
    data = {
        "document": {
            "content": text,
            "type": "PLAIN_TEXT"
        }
    }
    response = requests.post(url, json=data)
    sentiment = response.json().get('documentSentiment', None)
    return sentiment

# Generate a response based on the sentiment analysis result
def generate_response(text, sentiment):
    if sentiment is None:
        return "Hmm... I'm not sure what to say. Could you ask something else?"
    elif sentiment.get('score', 0) > 0.3:
        return "That's great to hear!"
    elif sentiment.get('score', 0) < -0.3:
        return "I'm sorry to hear that. Is there anything I can do to help?"
    else:
        # Basic logic to generate responses based on user input
        response = responses.get(text.lower())
        if response:
            return response
        elif "how are you" in text.lower():
            return "I'm just a computer program, so I don't have feelings, but thanks for asking!"
        elif "thank you" in text.lower():
            return "You're welcome!"
        else:
            return "Hmm... that's interesting."

# Function to edit a response
def edit_response():
    print("Which response would you like to edit?")
    phrase = listen().lower()
    if phrase in responses:
        print(f"The current response for '{phrase}' is: {responses[phrase]}")
        print("Please provide the new response:")
        new_response = listen()
        responses[phrase] = new_response
        save_responses()  # Save responses to file
        print("Response updated.")
    else:
        print("I couldn't find a response for that phrase.")

# Main function to run the program
def main():
    while True:
        text = listen()
        if text:
            if text.lower() == "jarvis edit":
                edit_response()
            else:
                sentiment = analyze_sentiment(text)
                response = generate_response(text, sentiment)
                print("Response:", response)
                if response not in responses.values():
                    print("AI: What should I respond to that?")
                    new_response = listen()
                    responses[text.lower()] = new_response
                    save_responses()  # Save responses to file
                    print("AI: Okay, got it.")

if __name__ == "__main__":
    main()
