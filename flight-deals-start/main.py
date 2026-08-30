# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.

from flight_search import FlightSearch
import flight_data
from data_manager import DataManager
from pprint import pprint
from notification_manager import NotificationManager


#
# token_results = search.get_access_token()
#
# if token_results["is_successful"]:
#     print(f"token: {token_results["access_token"]}")
#     print(f"expiration_time: {token_results["expiration_time"]}")

# search.get_city_code("Raleigh")

data_manager = DataManager()
search = FlightSearch()
data = flight_data.FlightData()

sheet_data = data_manager.read_entire_sheet()
# # pprint(sheet_data)
#
# # update the airport codes in Google Sheet
#
# for row in sheet_data:
#     if row["iataCode"] == "":
#         row["iataCode"] = search.get_city_code(row["city"])
#         # print(row["iataCode"])
#
# data_manager.destination_data = sheet_data
# data_manager.update_destination_code()

for row in sheet_data:
    print(f"Getting flights for {row['city']}")
    flight_results = search.search_for_flights(origin_code="MAD", destination_code=row["iataCode"], max_price=row["lowestPrice"])
    # pprint(flight_results)

    cheapest_flight = flight_data.find_cheapest_flight(flight_results)
    print(f"{row['city']}: {cheapest_flight.price}")

    if cheapest_flight.price != "N/A" and cheapest_flight.price <= row["lowestPrice"]:
        notification = NotificationManager()
        notification.send_message(recipient="bfutrel@gmail.com", price=cheapest_flight.price,
                                 departure_iata_code=cheapest_flight.origin_airport,
                                 arrival_iata_code=cheapest_flight.destination_airport,
                                 outbound_date=cheapest_flight.out_date, inbound_date=cheapest_flight.return_date)