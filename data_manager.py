from pprint import pprint
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/c97ddcf246b18fca233de42f8722e033/flightDeals/prices"


class DataManager:

    def __init__(self):
        self.SHEETY_USERNAME = os.getenv("ENV_SHEETY_USERNAME")
        self.SHEETY_PASSWORD = os.getenv("ENV_SHEETY_PASSWORD")
        self.destination_data = {}

    def get_destination_data(self):

        response = requests.get(url=SHEETY_PRICES_ENDPOINT ,auth=(self.SHEETY_USERNAME, self.SHEETY_PASSWORD) )
        data = response.json()
        self.destination_data = data["prices"]
        # pprint(data)
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)