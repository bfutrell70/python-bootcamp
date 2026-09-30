from InternetSpeedTwitterBot import InternetSpeedTwitterBot

"""
Day 51 - Complaining Twitter Bot

Using htts://www.speedtest.net to check the internet connection speed
Download and upload speed
- may take a couple of minutes
- once the test is complete, a result ID will be displayed and download / upload speed
- compare results to promised internet speeds
- if results are below promised internet speeds, log into X (or Y) to add a tweet

Posting on Y:
- click Login from the main page
    - anchor tag, class 'y-login-link'
"""

PROMISED_DOWN = 1000
PROMISED_UP = 1000

bot = InternetSpeedTwitterBot(PROMISED_DOWN, PROMISED_UP)
bot.tweet_at_provider()