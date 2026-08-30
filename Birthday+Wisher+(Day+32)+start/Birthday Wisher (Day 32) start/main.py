import datetime as dt
import random
import smtplib

def get_random_quote():
    """ get a random quote from quotes.txt and return it """
    with open("quotes.txt", "r") as file:
        quotes = file.readlines()
        r = random.Random()
        return r.choice(quotes)

def send_email(recipient, subject, body):
    """
    send an email with the subject and body to the specified recipient
    :param recipient: email address the email will be sent to
    :param subject: subject of the email
    :param body: body of the email
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
            msg=f"Subject: {subject}\n\n{body}")

# ------------------- main code -----------------------
now = dt.datetime.now()
year = now.year
month = now.month

# this is 0-based starting from Monday
day_of_week = now.weekday()

# send a random quote if the day of the week is Monday.
if day_of_week == 0:
    # send an email with a random quote
    quote = get_random_quote()
    send_email("wfutrell70@twc.com", "A quote for you", quote)

