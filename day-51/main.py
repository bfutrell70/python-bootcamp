import os
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

"""
Day 51 - Complaining Twitter Bot

Using htts://speedtest.net to check the internet connection speed
Download and upload speed
- may take a couple of minutes
- once the test is complete, a result ID will be displayed and download / upload speed
- compare results to promised internet speeds
- if results are below promised internet speeds, log into X (or Y) to add a tweet

Posting on Y:
- click Login from the main page
    - anchor tag, class 'y-login-link'
"""

Y_EMAIL_ADDRESS = 'bfutrel@gmail.com'
Y_PASSWORD = 'X-QdVDC1C1j-TPKo'
Y_URL = 'https://app.100daysofpython.dev/services/y'

PROMISED_DOWN = 1000
PROMISED_UP = 1000

# configure Selenium
chrome_options = webdriver.ChromeOptions()
# if True must close Chrome manually before the script is re-run
chrome_options.add_experimental_option("detach", True)

# have Selenium create its own user profile
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")

# tell the Chrome driver to use the user data directory specified above
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Set up the Chrome WebDriver (make sure chromedriver is installed and in PATH)
driver = webdriver.Chrome(chrome_options)

driver.get(Y_URL)
time.sleep(2)