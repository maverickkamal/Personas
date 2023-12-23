import requests

class BirthDataCalculator:
    def __init__(self, birth_date, birth_time, latitude, longitude):
        self.url = 'https://hexivium-api-637a6012f8f4.herokuapp.com/calculate'
        self.data = {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "latitude": latitude,
            "longitude": longitude
        }

    def calculate_birth_data(self):
        try:
            response = requests.post(self.url, json=self.data)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Error: {response.status_code}, {response.text}"}
        except Exception as e:
            return {"error": f"An exception occurred: {str(e)}"}
