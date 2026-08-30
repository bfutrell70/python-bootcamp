capitals = {
    "France": "Paris",
    "Germany": "Berlin"
}

# nested list in dictionary

# travel_log = {
#     "France": ["Paris", "Lille", "Dijon"],
#     "Germany": ["Stuttgart", "Berlin"]
# }

# pause 1
# print(travel_log["France"][1])

nested_list = ["A", "B", ["C", "D"]]

# pause 2
print(nested_list[2][1])

travel_log = {
  "France": {
    "cities_visited": ["Paris", "Lille", "Dijon"],
    "total_visits": 12
   },
  "Germany": {
    "cities_visited": ["Berlin", "Hamburg", "Stuttgart"],
    "total_visits": 5
   },
}

# pause 3
print(travel_log["Germany"]["cities_visited"][2])