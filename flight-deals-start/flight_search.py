from http.client import HTTPException
from pprint import pprint

import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flight_data import FlightData
# from urllib.error import HTTPError

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    # two API endpoints used:
    # Flight Offers Search - https://test.api.amadeus.com/v2/shopping/flight-offers
    #   reference - https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference
    #   this API endpoint has a currencyCode property that specifies the currency being returned
    # 6/10/2025 don't use Flight Offers Search - it doesn't allow for date ranges in the API call.
    # use the Flight Cheapest Date search, which does allow for date ranges.

    # City Search - https://test.api.amadeus.com/v1/reference-data/locations/cities
    #   reference - https://developers.amadeus.com/self-service/category/destination-experiences/api-doc/city-search/api-reference

    # Flight Cheapest Date Search - https://test.api.amadeus.com/v1/shopping/flight-dates
    #   reference - https://developers.amadeus.com/self-service/category/flights/api-doc/flight-cheapest-date-search/api-reference
    #   NOTE: what currency is the price in? Appears to be USD.

    # Flight Inspiration Search - https://test.api.amadeus.com/v2/shopping/flight-destinations
    #   reference - https://developers.amadeus.com/self-service/category/flights/api-doc/flight-inspiration-search/api-reference
    #   results are ordered by price

    # 6/12/2025 - based on the API documentation, use them in the following order:
    #           1 - Flight Inspiration to find the cheapest flight destinations from a specific city
    #           2 - Flight Offers Search to search for flights once a destination is chosen
    #           3 - Flight Cheapest Date Search to check for the cheapest dates to fly


    # must authenticate using OICD - https://test.api.amadeus.com/v1/security/oauth2/token
    #   reference - https://developers.amadeus.com/self-service/apis-docs/guides/developer-guides/API-Keys/authorization/

    def __init__(self):
        load_dotenv()
        self.AMADEUS_API_KEY = os.environ["AMADEUS_API_KEY"]
        self.AMADEUS_API_SECRET = os.environ["AMADEUS_API_SECRET"]
        self.AMADEUS_AUTH_URL = os.environ["AMADEUS_AUTH_URL"]
        self.AMADEUS_FLIGHT_SEARCH_URL = os.environ["AMADEUS_FLIGHT_SEARCH_URL"]
        self.AMADEUS_CITY_SEARCH_URL = os.environ["AMADEUS_CITY_SEARCH_URL"]
        self.AMADEUS_FLIGHT_CHEAPEST_DATE_SEARCH_URL = os.environ["AMADEUS_FLIGHT_CHEAPEST_DATE_SEARCH_URL"]
        self.access_key = ""
        self.expiration_time = datetime.now()

        # will set the access_key and expiration_time properties
        self._get_access_token()

    def _get_access_token(self):
        """
        authenticate using OIDC before performing an API call
        :return: True if successful, False if not successful
        """
        body = {
            "grant_type": "client_credentials",
            "client_id": self.AMADEUS_API_KEY,
            "client_secret": self.AMADEUS_API_SECRET
        }

        # to send a post request in x-www-form-urlencoded, using the data parameter
        # if sending data in plain text it would use the json parameter
        result = requests.post(url=self.AMADEUS_AUTH_URL, data=body)
        # print(result.text)
        result.raise_for_status()

        response = result.json()
        if response["state"] == "approved":
            self.expiration_time = datetime.now() + timedelta(seconds=int(response["expires_in"]))
            self.access_key = response["access_token"]
            return True
        else:
            return False

    def get_city_code(self, city_name):
        """
        get the airport codes associated with a city
        :param city_name: name of a city to get airport codes for
        :return: string containing IATA code if the city has one, None if it doesn't or there was an error
        """
        if self.expiration_time < datetime.now():
            success = self._get_access_token()

            if not success:
                return "Error occurred when getting the access token"

        headers = {
            "Authorization": f"Bearer {self.access_key}"
        }

        params = {
            "keyword": city_name,
            "max": 1
        }

        # use GET API endpoint
        # looking for IATA codes in the result
        # results in "data"
        # number of results in ["meta"]["count"]
        # within each result:
        #   ["name"]: city name
        #   ["iataCode"]: if a result doesn't have an airport this will not be in the result
        #   ["address"]: contains address information
        #   ["address"]["countryCode"] country code for the result
        #   ["address"]["stateCode"] state code for the result - prefixed with '<country code>-'

        try:
            response = requests.get(url=self.AMADEUS_CITY_SEARCH_URL, headers=headers, params=params)
            response.raise_for_status()

            print("--- get_city_code result ---")
            print(response.text)

            data = response.json()["data"]
            # verify the iataCode is present before returning it
            code = data[0]["iataCode"]
        except IndexError:
            print(f"IndexError: no airport code found for {city_name}")
            return "N/A"
        except KeyError:
            print(f"KeyError: no airport code found for {city_name}")
            return "N/A"

        except requests.exceptions.HTTPError as e:
            print(e)
            return None
        else:
            return code

    def search_for_flights(self, origin_code, destination_code, max_price):
        """
        search for flights between the two cities by their IATA code
        :param origin_code: origin IATA code
        :param destination_code: destination IATA code
        :param max_price: max price of flight
        :return:
        """
        # check if expiration time has elapsed
        # if so get a new access token
        if self.expiration_time < datetime.now():
            success = self._get_access_token()

            if not success:
                return "Error occurred when getting the access token"

        headers = {
            "Authorization": f"Bearer {self.access_key}"
        }

        now = datetime.now()
        start_delta = timedelta(days=1)
        end_delta = timedelta(days=180)

        # have to add a timedelta to a datetime in order to get a datetime object as a result
        # just doing start_date = now + timedelta(days=1) returned a timedelta object
        start_date = now + start_delta
        end_date = start_date + end_delta

        date_range = f"{start_date.strftime("%Y-%m-%d")},{end_date.strftime("%Y-%m-%d")}"

        # use GET API endpoint

        params = {
            "origin": origin_code,
            "destination": destination_code,
            "departureDate": date_range
        }

        try:
            response = requests.get(url=self.AMADEUS_FLIGHT_CHEAPEST_DATE_SEARCH_URL, headers=headers, params=params)
            response.raise_for_status()

            flight_info = response.json()
            # print(flight_info)
            flights = []

            # build a list of flights
            for flight in flight_info["data"]:
                """
                ["data"]
                    ["origin"]
                    ["destination"]
                    ["departureDate"]
                    ["returnDate"]
                    ["price"]["total"]
                    ["links"]["flightOffers"] - URL to get the live price, need to add 'currencyCode=GBP' to it to return price in Pounds
                    
                ["dictionaries"]["currencies"] - key indicates type of currency
                """
                new_flight = FlightData()
                new_flight.price = float(flight["price"]["total"])
                new_flight.out_date = flight["departureDate"]
                new_flight.return_date = flight["returnDate"]
                new_flight.origin_airport = flight["origin"]
                new_flight.destination_airport = flight["destination"]
                # contains an API URL to the Flight Offers Search API endpoint
                # Will need to add "currencyCode=GBP" to the end of the URL to meet
                # the requirements in "lecture" 297.
                new_flight.flight_offers = flight["links"]["flightOffers"]
                flights.append(new_flight)

            # now that we have a list of flights, need to
            # order them by price, then see if any of them are

            # pprint(flights)

            return flights


        except requests.exceptions.HTTPError as e:
            # print(e)

            flight_data = FlightData()

            flight_data.out_date = "N/A"
            flight_data.return_date = "N/A"
            flight_data.price = "N/A"
            flight_data.origin_airport = "N/A"
            flight_data.destination_airport = "N/A"

            return [flight_data]
        except Exception as x:
            print(x)