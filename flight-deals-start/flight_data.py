class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        self.price = ""
        self.origin_airport = ""
        self.destination_airport = ""
        self.out_date = ""
        self.return_date = ""
        self.flight_offers = ""

def find_cheapest_flight(flights):
    """
    find the cheapest flight from the list of flights
    :param flights: list of flights from the Flight Cheapest Date Search API
    :return: cheapest flight in the list
    """

    def get_price(e):
        return e.price

    if flights is not None:

        sorted_flights = sorted(flights, key=get_price)
        # print(sorted_flights)

        cheapest_flight = flights[0]
        for flight in flights:
            if flight.price < cheapest_flight.price:
                cheapest_flight = flight

        return cheapest_flight
    else:
        return None