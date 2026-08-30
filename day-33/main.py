import requests
import json
from datetime import datetime

# response = requests.get(url="http://api.open-notify.org/iss-now.json")
# # raises an exception if the request wasn't successful
# response.raise_for_status()
#
# # prints response HTTP Status Code
# print(response)
#
# data = response.json()
#
# # data returned from the API request is in the content property
# print(data)
# iss_position = (data["iss_position"]["latitude"], data["iss_position"]["longitude"])
#
# print(iss_position)

MY_LAT = 35.781300
MY_LONG = -78641678
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
    "tzid": "America/New_York"
}
response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()

# split the sunrise date/time by T, time is the element at index 1
sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
sunset = data["results"]["sunset"].split("T")[1].split(":")[0]

print(f"Sunrise: {sunrise}")
print(f"Sunset:  {sunset}")

time_now = datetime.now()
print(time_now)
print(response.url)
pretty_json = json.dumps(data, indent=4)
print(pretty_json)

