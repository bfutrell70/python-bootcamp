import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import smtplib

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        load_dotenv()
        self.GOOGLE_ACCOUNT = os.environ["GMAIL_EMAIL_ADDRESS"]
        self.GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]

    def send_message(self, recipient, price, departure_iata_code, arrival_iata_code, outbound_date, inbound_date):
        """
        send an email with flight information to a user
        :param recipient: recipient's email address
        :param price: flight price
        :param departure_iata_code: IATA code of the departure airport
        :param arrival_iata_code: IATA code of the arrival airport
        :param outbound_date: date of departure
        :param inbound_date: date of return
        :return:
        """
        with smtplib.SMTP('smtp.gmail.com') as connection:
            # secures connection to email server - uses TLS
            connection.starttls()

            # login to email server
            connection.login(self.GOOGLE_ACCOUNT, self.GMAIL_APP_PASSWORD)

            message = (f"Low price alert!\nOnly {price} to fly from {departure_iata_code} to {arrival_iata_code},"
                       f"on {outbound_date} until {inbound_date}")

            # msg contains the subject and message as part of the msg parameter
            # contents of msg parameters: 'Subject: <subject here>\n\n<message body>'
            connection.sendmail(
                from_addr=self.GOOGLE_ACCOUNT,
                to_addrs=recipient,
                msg=f"Subject: Low Price Alert!\n\n{message}")
