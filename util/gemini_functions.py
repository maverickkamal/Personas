import os
import requests

url = 'https://hexivium-api-637a6012f8f4.herokuapp.com/calculate'

def get_personality(birth_date, birth_time, latitude, longitude):
    data = {
        "birth_date": birth_date,
        "birth_time": birth_time,
        "latitude": latitude,
        "longitude": longitude
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        datas = response.json()
        return datas
    else:
        return {"error": f"Error: {response.status_code}, {response.text}"}

definitions = [
    {
        "name": "get_personality",
        "description": "returns Persons personality base on birth date, time, latitude and logitude in a structured json format",
        "parameters": {
            "type": "object",
            "properties": {
                "birth_date": {
                    "type": "string",
                    "description": "Persons date of birth"
                },
                "birth_time": {
                    "type": "string",
                    "description": "Persons time of birth"
                },
                "latitude": {
                    "type": "integer",
                    "description": "Persons latitude"
                },
                "longitude": {
                    "type": "integer",
                    "description": "Persons longitude"
                }
            }
        }
    }
]
