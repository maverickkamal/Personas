import streamlit as st
import requests
import json
import sys
import os
from dotenv import load_dotenv
import gemini_functions

avatar = "https://media.roboflow.com/spaces/gemini-icon.png"
avatar2 = "https://i.ibb.co/8BKfNPx/avatar.png"
st.set_page_config(
    page_title="ZENTiDE - Personality Match", page_icon=avatar)
load_dotenv()
#api_key = os.getenv("GEMINI_API_KEY")
api_key = st.secrets["GOOGLE_API_KEY"]

def parse_function_response(message):
    function_call = message[0]["functionCall"]
    function_name = function_call["name"]

    #print("Gemini: Called function " + function_name )

    try:
        arguments = function_call["args"]

        if hasattr(gemini_functions, function_name):
            function_response = getattr(gemini_functions, function_name)(**arguments)
        else:
            function_response = "ERROR: Called unknown function"
    except TypeError:
        function_response = "ERROR: Invalid arguments"

    return (function_name, function_response)


def run_conversation(message, messages = []):
    messages.append(message)
    with st.chat_message("user", avatar=avatar2):
        st.markdown(prompt)
    with st.chat_message("model", avatar=avatar):
        with st.spinner('Generating...'):
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
        	#print(response.text)
        	#print("ERROR: Unable to make request")
        	sys.exit(1)

    	response = response.json()
    	if "candidates" in response and response["candidates"]:
       		if "content" not in response["candidates"][0]:
           		print("ERROR: No content in response")
           		#print(response)
           		#sys.exit(1)

    	message = response["candidates"][0]["content"]["parts"]
    	messages.append({
        	"role": "model",
        	"parts": message
   	 })

    	if "functionCall" in message[0]:
        	function_name, function_response = parse_function_response(message)

        	message = {
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
    	else:
        	user_message = input("Gemini: " + message[0]["text"] + "\nYou: ")
        	message = {
            	"role": "user",
            	"parts": [{"text": user_message}]
        	}

    run_conversation(message, messages)
    return response.text


start_message = st.chat_message("model", avatar=avatar)
start_message.write(
    "Hello friend, I am your Personality assisstant. Let's find out your Personas")
messages = []

system_message = "You are an AI bot that can do everything using function calls. When you are asked to do something, use the function call you have available and then respond with a message shortly confirming what you have done. When writing Personality, Summarize the key aspects of the persons character in a Table or dataframe while keping it personal. When writing the Personality, Make it motivational by telling the person about their inner self."

for sms in messages:
    with st.chat_message(sms["role"], avatar=(avatar if sms["role"] == "model" else (avatar2 if sms["role"] == "user" else None))):
        st.markdown(sms[0]["text"])
		
chat_input_box = st.chat_input("what's on your mind??")
#user_message = input("Gemini: What do you want to do?\nYou: ")
message = {
    "role": "user",
    "parts": [{"text": system_message + "\n\n" + user_message}]
}

if chat_input_box:
    response = run_conversation(message, messages)
	st.markdown(response)

#print(response)

