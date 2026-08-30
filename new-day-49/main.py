import os

import selenium.common
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.support.wait import WebDriverWait

"""
I can't remember what the goal for day 49 was previously, but I do remember
that the video and site it accessed was several years old.

Current goals:
- log in automatically into the Snack & Lift website
  https://appbrewery.github.io/gym/
- book specific gym classes
- handle waitlists
- deal with network errors like a pro
"""

ACCOUNT_EMAIL = 'bfutrel@gmail.com'
ACCOUNT_PASSWORD = 'Iw@nnaRipped!'
GYM_URL = 'https://appbrewery.github.io/gym/'
CLASS_SCHEDULE_URL = 'https://appbrewery.github.io/gym/schedule/'

"""
get the day of week from the date string
:param date: string containing the date
:returns day of week in lower case
"""
def get_day_of_week(date: str):
    # the date could be encased in parentheses if the date is today or tomorrow
    # today: 'Today (<day of week>, <month> <day of month>)'
    # tomorrow: 'Tomorrow (<day of week>, <month> <day of month>)'
    trimmed_date = date.replace('Today (', '').replace('Tomorrow (', '')

    dow = trimmed_date.lower()[0:3]
    return dow

"""
determine if the day is Tuesday
:param date: string containing the day of week
:returns True if the day of week is Tuesday, False if not
"""
def is_date_tuesday(date: str):
    if date == 'tue':
        return True

    return False


# configure Selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# have Selenium create its own user profile
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")

# tell the Chrome driver to use the user data directory specified above
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Set up the Chrome WebDriver (make sure chromedriver is installed and in PATH)
driver = webdriver.Chrome(chrome_options)
driver.get(GYM_URL)

"""
step 2
- click the login button
    - ID 'login-button'
- fill in your email and password
    - email input ID 'email-input'
    - password input ID 'password-input'
- submit the form
    - submit button ID 'submit-button'
- verify you're logged in by checking for the "Class Schedule" page
    - once logged in, redirected to the class schedule page
    - https://appbrewery.github.io/gym/schedule/
"""

login_button = driver.find_element(By.CSS_SELECTOR, '#login-button')
login_button.click()

# Login page - enter the username/password and click Submit
email_input = driver.find_element(By.CSS_SELECTOR, '#email-input')

wait = WebDriverWait(driver, timeout = 2)
wait.until(lambda _ : email_input.is_displayed())

email_input.send_keys(ACCOUNT_EMAIL)

password_input = driver.find_element(By.CSS_SELECTOR, '#password-input')
password_input.send_keys(ACCOUNT_PASSWORD)

current_webpage = driver.current_url

submit_button = driver.find_element(By.CSS_SELECTOR, '#submit-button')
submit_button.click()

# once logged in, redirected to the class schedule page
wait = WebDriverWait(driver, timeout = 10).until(EC.url_changes(current_webpage))

# find the next Tuesday 6pm class (any type - Yoga, Spin, or HIIT)
"""
markup for days
div id = "day-group-today-(thu,-aug-20)"        [container for classes for the day]
    h2 id = "day-title-today-(thu,-aug-20)"     [name of date]
    div id = "class-card-hiit-2026-08-20-0900"  [card representing a single exercise class]
div id = "day-group-tomorrow-(fri,-aug-21)"
    h2 id = "day-title-tomorrow-(fri,-aug-21)"
    div id = "class-card-yoga-2026-08-22-0700"
div id = "day-group-sat,-aug-22"
    h2 id = "day-title-sat,-aug-22"
    div id = "class-card-yoga-2026-08-22-0700"
"""

# # --- approach 1 - get the div elements representing each day, find the one for Tuesday.
# # get div elements representing each day
# # element 0 will be for the current date
# print('--- finding date by getting day containers')
# day_groups = driver.find_elements(By.CSS_SELECTOR, 'div[id^="day-group-"]')
# for day_groups_index in range(len(day_groups)):
#     day_group = day_groups[day_groups_index]
#
#     # get h2 element
#     title = day_group.find_element(By.CSS_SELECTOR, 'h2')
#
#     # find the day in the element
#     day_text = title.text
#
#     print(day_text)


# --- approach 2 - get the div elements representing each class, then search parents to find the date
# --- this method appears to be what the hints in the section are pointing to
# get div elements representing each class
print('--- finding date by getting class containers')

def find_tuesday_div():
    tuesday_div_id = ''

    class_cards = driver.find_elements(By.CSS_SELECTOR, 'div[id^="class-card-"]')
    for class_cards_index in range(len(class_cards)):
        card = class_cards[class_cards_index]

        # get ID of the exercise class div
        class_card_id = card.get_attribute("id")
        if class_card_id is not None:
            # Without something limiting the search results for ancestors, any element containing
            # the class card div will be returned.
            # The element in index 0 will be the highest-level element matching the search criteria.
            # The element in the highest index will be the element that directly contains the specified element.

            # We want the last index, which is the div element containing the classes for a day.
            # Within the div element, there is an H2 tag with a class of 'Schedule_dayTitle__YBybs'
            # and an ID in the format 'day-title-<day of week>,-<month>-<day of month>'
            xpath = f"//div[@id='{class_card_id}']/ancestor::div"
            ancestors = driver.find_elements(By.XPATH, xpath)

            container = ancestors[-1]
            h2_element = container.find_element(By.CSS_SELECTOR, 'h2')

            # day text within the H2 tag is in the format '<day of week (len=3)>, <month (len=3)> <day of month>'
            day = h2_element.text
            day_of_week = get_day_of_week(day)
            if is_date_tuesday(day_of_week) == True:
                # print('Tuesday found!')
                tuesday_div_id = container.get_attribute("id")
                break

        if tuesday_div_id != '':
            break

    return tuesday_div_id


print(f'ID of div for Tuesday: [{find_tuesday_div()}]')