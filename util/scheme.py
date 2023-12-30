import requests
import json
import sys
import os
from dotenv import load_dotenv
import gemini_functions

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def parse_function_response(message):
    function_call = message[0]["functionCall"]
    function_name = function_call["name"]

    try:
        arguments = function_call["args"]

        if hasattr(gemini_functions, function_name):
            function_response = getattr(gemini_functions, function_name)(**arguments)
        else:
            function_response = "ERROR: Called unknown function"
    except TypeError:
        function_response = "ERROR: Invalid arguments"

    return (function_name, function_response)

def run_function_call(message, messages):
    function_name, function_response = parse_function_response(message)

    function_message = {
        "role": "function",
        "parts": [{
            "functionResponse": {
                "name": function_name,
                "response": {
                    "name": function_name,
                    "content": function_response
                }
            }
        }]
    }

    messages.append(function_message)

def run_conversation(user_message, messages):
    system_message = "You are an AI bot that can do everything using function calls. When you are asked to do something, use the function call you have available and then respond with a message shortly confirming what you have done. When writing Personality, Summarize the key aspects of the person's character in a Table or dataframe while keeping it personal. When writing the Personality, Make it motivational by telling the person about their inner self."

    initial_message = {
        "role": "user",
        "parts": [{"text": system_message + "\n\n" + user_message}]
    }

    messages.append(initial_message)

    while True:
        with open("messages.json", "w") as f:
            f.write(json.dumps(messages, indent=4))

        data = {
            "contents": [messages],
            "tools": [{
                "functionDeclarations": gemini_functions.definitions
            }]
        }

        response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key="+api_key, json=data)

        if response.status_code != 200:
            print("ERROR: Unable to make request")
            sys.exit(1)

        response = response.json()
        if "candidates" in response and response["candidates"]:
            if "content" not in response["candidates"][0]:
                print("ERROR: No content in response")
                sys.exit(1)

        message = response["candidates"][0]["content"]["parts"]
        messages.append({
            "role": "model",
            "parts": message
        })

        if "functionCall" in message[0]:
            run_function_call(message, messages)
        else:
            user_response = input("Gemini: " + message[0]["text"] + "\nYou: ")
            user_message = {
                "role": "user",
                "parts": [{"text": user_response}]
            }
            messages.append(user_message)

        #if "functionCall" not in message[0]:
          #  break

    return response

#messages = []

#user_input = input("Gemini: What do you want to do?\nYou: ")
#run_conversation(user_input, messages)
#run_conversation(user_input, messages)

#print(messages)
