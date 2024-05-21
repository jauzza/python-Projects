import json
import random

# Function to load data from JSON file
def load_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {"conversations": [], "responses": {}}
    return data

# Function to save data to JSON file
def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Function to get response from the bot
def get_response(user_input, data):
    responses = data["responses"]
    if user_input.lower() in responses:
        return random.choice(responses[user_input.lower()])
    else:
        return "I'm sorry, I don't understand that."

# Main function
def main():
    data_file = "chatbot_data.json"
    data = load_data(data_file)

    print("Welcome to the ChatBot! Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        response = get_response(user_input, data)
        print("Bot:", response)

        # Log the conversation
        data["conversations"].append({"user_input": user_input, "bot_response": response})

        # Learn from the conversation
        if user_input.lower() not in data["responses"]:
            new_response = input("What should I respond to that? ")
            data["responses"][user_input.lower()] = [new_response]
        elif response not in data["responses"][user_input.lower()]:
            data["responses"][user_input.lower()].append(response)

        save_data(data, data_file)

if __name__ == "__main__":
    main()
