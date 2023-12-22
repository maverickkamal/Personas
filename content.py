import requests
import streamlit as st

url = 'https://hexivium-api-637a6012f8f4.herokuapp.com/calculate'


data = {
    "birth_date": "06/10/1988",
    "birth_time": "21:30",
    "latitude": 6.0,
    "longitude": 35.0
}

#Make the GET request
response = requests.post(url, json=data)


if response.status_code == 200:
    # Print the response data
    print("Response from server:", response.json())
else:
    # Print an error if something went wrong
    print("Error:", response.status_code, response.text)
