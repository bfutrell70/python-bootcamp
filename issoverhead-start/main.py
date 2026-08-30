import requests
from datetime import datetime
import smtplib
import threading
import time

from requests import HTTPError


def send_email():
    """ sends an email that the IIS is close to you """
    print("in send_email")
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
            to_addrs=my_email,
            msg=f"Subject: The ISS is close!\n\nThe ISS is close to you - look up!")


MY_LAT = 35.781300 # Your latitude
MY_LONG = -78.641678 # Your longitude

def is_iss_overhead():
    """ returns True if the IIS is close to me, False if not """
    print("in check_iss_position")
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.

    if (MY_LAT - 5) <= iss_latitude <= (MY_LAT + 5) and (MY_LONG - 5) <= iss_longitude <= (MY_LONG + 5):
        return True
    else:
        return False

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
        "tzid": "America/New_York"
    }

    try:
        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()
        data = response.json()
        sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

        print(f"sunrise: {sunrise}")
        print(f"sunset: {sunset}")

        time_now = datetime.now()

        if sunset <= time_now.hour <= sunrise:
            return True
        else:
            return False

    except HTTPError:
        return False


def check_iss_position():
    """ checks if the IIS is close to me, and if it is and it is dark send an email"""
    iss_overhead = is_iss_overhead()
    is_it_dark = is_night()
    
    if iss_overhead and is_it_dark:
        # send email
        print("ISS is close...")
        send_email()

def run_every_minute():
    """ schedules an event to run every 60 seconds """
    check_iss_position()
    threading.Timer(60, run_every_minute).start()

# start the timer
run_every_minute()

# keep the main thread alve to allow the timer to run
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated")