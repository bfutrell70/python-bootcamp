import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

URL = "https://appbrewery.github.io/instant_pot/"

TARGET_PRICE = 100
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
ACCEPT_LANGUAGE = "en-US,en;q=0.5"

load_dotenv()
SMTP_SERVER = os.environ['SMTP_SERVER']
EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
PASSWORD = os.environ['PASSWORD']

response = requests.get(URL)
page_data = response.text

soup = BeautifulSoup(markup=page_data, features='html.parser')

# get price from Amazon clone product page
dollars = soup.select_one('span.a-price-whole').text
cents = soup.select_one('span.a-price-fraction').text
price = float(f"{dollars}{cents}")
print(price)

if price < TARGET_PRICE:
    # price is lower than the target price - send an email
    with smtplib.SMTP(SMTP_SERVER) as connection:
        # connect to email server with TLS
        connection.starttls()

        # login to email server
        connection.login(EMAIL_ADDRESS, PASSWORD)

        product_name = soup.select_one('#productTitle').text
        message = (f"Subject: Low Price Alert!\n\nProduct price alert!\n\n{product_name} is now ${price}\n"
                   f"{URL}")

        print(message)

        connection.sendmail(
            from_addr=EMAIL_ADDRESS,
            to_addrs=[EMAIL_ADDRESS], msg=message.encode('utf-8'))
