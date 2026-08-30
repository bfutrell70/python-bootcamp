import datetime
import os
from dotenv import load_dotenv
import requests
import smtplib
from datetime import datetime, timedelta

load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ["STOCK_API_KEY"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]

def send_email(recipient, stock_name, heading, description):
    """
    send an email with the subject and body to the specified recipient
    :param recipient: email address the email will be sent to
    :param stock_name: name of the stock to get data for
    :param heading: news article header
    :param description: news article description
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
            msg=f"Subject: Stock news....\n\n{stock_name}\n\nHeading: {heading}\nSummary: {description}")

def get_stock_prices():
    """
    gets stock prices for the previous two days

    returns:
    a tuple with two floats
        - first item is yesterday's closing price
        - second item is the closing price two days ago
    """

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
        "outputsize": "compact",
        "apikey": STOCK_API_KEY
    }

    response = requests.get(STOCK_ENDPOINT, params=params)
    response.raise_for_status()

    stock_data = response.json()
    print(stock_data)
    daily_items = stock_data["Time Series (Daily)"]

    closing_prices = [float(value["4. close"]) for (key, value) in daily_items.items()]

    first_price = closing_prices[0]
    second_price = closing_prices[1]

    return first_price, second_price

def get_news():
    """
    get news articles from the past week for Tesla
    :return: the first three articles from the API response
    """
    now = datetime.now()
    now = now - timedelta(days=7)
    params = {
        "q": COMPANY_NAME,
        "searchIn": "title",
        "from": f"{now.year}-{now.month}-{now.day}",
        "sortBy": "popularity",
        "apiKey": NEWS_API_KEY,
        "pageSize": 5
    }
    result = requests.get(NEWS_ENDPOINT, params=params)
    result.raise_for_status()

    articles = result.json()
    return articles["articles"][:3]

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
# e.g. [new_value for (key, value) in dictionary.items()]
# yesterday is the first key in the dictionary


#TODO 2. - Get the day before yesterday's closing stock price
(yesterday_price, day_before_price) = get_stock_prices()

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
# Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(yesterday_price - day_before_price)
print(f"difference: {difference}")

percentage_difference = difference / yesterday_price * 100
print(f"percentage difference: {percentage_difference}")

if percentage_difference > 0.5:
    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
    relevant_articles = get_news()

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number (or email).

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    summaries = [{"headline": value["title"], "description": value["description"]} for value in relevant_articles]
    print("summaries")
    print(summaries)

#TODO 9. - Send each article as a separate message via Twilio. 

    for summary in summaries:
        # having to convert to UTF-8 since email doesn't seem to handle Unicode.

        send_email(
            recipient="bfutrel@gmail.com",
            stock_name=STOCK_NAME,
            heading=summary["headline"].encode("utf-8", "ignore"),
            description=(summary["description"] or "").encode("utf-8", "ignore")
        )

    print("Sent articles to email")


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

