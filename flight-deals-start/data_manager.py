import requests
import os
from dotenv import load_dotenv
from datetime import datetime

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    # uses the Sheety API
    # https://api.sheety.co/a7c1bf7011705884125c54538c053929/flightDeals/prices
    # uses bearer token
    # enabled get, add, and edit functionality

    def __init__(self):
        load_dotenv()
        self.SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]
        self.SHEETY_URL = os.environ["SHEETY_URL"]
        self.destination_data = {}

    def read_entire_sheet(self):
        """
        reads the rows from the Google Sheet
        :return: JSON object representing the data from the sheet
        """

        headers = {
            "Authorization": f"Bearer {self.SHEETY_TOKEN}"
        }

        result = requests.get(url=self.SHEETY_URL, headers=headers)
        # print(result.text)

        self.destination_data = result.json()["prices"]

        return self.destination_data

    def update_destination_code(self):
        """
        updates the IATA code for the specified row in the sheet
        :return:
        """

        headers = {
            "Authorization": f"Bearer {self.SHEETY_TOKEN}"
        }

        for row in self.destination_data:
            if row["iataCode"] != "":
                url = f"{self.SHEETY_URL}/{row["id"]}"
                body = {
                    "price":
                    {
                        "iataCode": row["iataCode"]
                    }
                }

                response = requests.put(url=url, headers=headers, json=body)
                print(response.text)