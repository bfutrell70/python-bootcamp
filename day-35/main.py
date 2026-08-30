import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

# API_KEY = "c9be39040d13c1066a2530f730696158"
API_KEY = os.environ["OWN_API_KEY"]
LATITUDE = 35.879833
LONGITUDE = -78.503855

# url = f"http://api.openweathermap.org/data/2.5/forecast?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}"
OWN_Endpoint = "http://api.openweathermap.org/data/2.5/forecast"

weather_params = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "cnt": 4,       # getting the first 4 forecasts for the next 12 hours
    "appid": API_KEY
}

def send_email(recipient):
    """
    send an email with the subject and body to the specified recipient
    :param recipient: email address the email will be sent to
    """
    my_email = "bfutrel@gmail.com"
    password = 'nepo tswx xvho eige'
    with smtplib.SMTP('smtp.gmail.com') as connection:
        # secures connection to email server - uses TLS
        connection.starttls()

        # login to email server
        connection.login(my_email, password)

        # msg contains the subject and message as part of the msg parameter
        # contents of msg parameters: 'Subject: <subject here>\n\n<message body>'
        connection.sendmail(
            from_addr=my_email,
            to_addrs=recipient,
            msg=f"Subject: Bring an umbrella!\n\nThere is a chance of rain in the next 12 hours.")

# request = requests.get(method="get", url=url)
response = requests.get(url=OWN_Endpoint, params=weather_params)
response.raise_for_status()

weather_data  = response.json()
print(f"status code: {response.status_code}")
print(f"response: {weather_data}")

# date/time string stored in the field "dt_txt"
# date/time value stored in the field "dt"
# weather info stored in "weather" part of results. it has 4 members:
#   - id [int]
#   - main [string] - appears to be a broad description of the weather - UNIX timestamp - # of seconds since 1/1/1970
#   - description - appears to be a more detailed description of the weather
# can be multiple weather conditions for a location
# major weather event will be first in the list
# ID of less than 700 will require an umbrella

print(len(weather_data["list"]))


will_rain = False

for forecast in weather_data["list"]:
    # print(forecast["weather"])
    # print(forecast["dt_txt"])
    for weather in forecast["weather"]:
        if weather["id"] < 700:
            will_rain = True

if will_rain:
    # print("Bring an umbrella!")
    send_email("bfutrel@gmail.com")