"""
Make changes for step 6 in this file
- book EVERY Tuesday AND Thursday 6pm class
- keep track of all classes processed
- print a detailed list of what happened

Make changes for step 7
- Comment out "Booking Summary" for now
- navigate to the "My Bookings" page
- Count all Tuesday/Thursday 6pm bookings
- compare the results with what you tried to book
- print the verification results


"""

import os
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from class_booking_info import ClassBookingInfo

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
BOOKING_SUMMARY_URL = 'https://appbrewery.github.io/gym/my-bookings/'

new_bookings = 0
waitlists_joined = 0
already_booked_waitlisted = 0
detailed_class_list: list[ClassBookingInfo] = []

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
driver.get(GYM_URL)

"""
get the day of week from the date string
:param date: string containing the date
:returns three-letter day of week in lower case
"""


def get_day_of_week(date: str):
    # the date could be encased in parentheses if the date is today or tomorrow
    # today: 'Today (<day of week>, <month> <day of month>)'
    # tomorrow: 'Tomorrow (<day of week>, <month> <day of month>)'
    trimmed_date = date.replace('Today (', '').replace('Tomorrow (', '')

    dow = trimmed_date.lower()[0:3]
    return dow


"""
determine if the day is in the list of days
:param date: string containing day of week
:param days_of_week: list of days of week
:returns True if day of week is in days_of_week, False if not
"""


def does_date_match(date: str, days_of_week):
    if date in days_of_week:
        return True

    return False


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

"""
log into the site
"""


def login():
    login_button = driver.find_element(By.CSS_SELECTOR, '#login-button')
    login_button.click()

    # Login page - enter the username/password and click Submit
    email_input = driver.find_element(By.CSS_SELECTOR, '#email-input')

    wait = WebDriverWait(driver, timeout=2)
    wait.until(lambda _: email_input.is_displayed())

    email_input.send_keys(ACCOUNT_EMAIL)

    password_input = driver.find_element(By.CSS_SELECTOR, '#password-input')
    password_input.send_keys(ACCOUNT_PASSWORD)

    current_webpage = driver.current_url

    submit_button = driver.find_element(By.CSS_SELECTOR, '#submit-button')
    submit_button.click()

    # once logged in, redirected to the class schedule page
    wait = WebDriverWait(driver, timeout=10).until(EC.url_changes(current_webpage))


# find the next Tuesday 6pm class (any type - Yoga, Spin, or HIIT)

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

"""
find IDs of div elements for the specified days of the week
:param days_of_week - list of strings containing the days of the week to find (['mon', 'tue', etc.])
:returns - list of div elements containing IDs for the specified days of the week
"""


def find_day_divs(days_of_week):
    day_div_ids = []

    class_cards = driver.find_elements(By.CSS_SELECTOR, 'div[id^="class-card-"]')
    for class_cards_index in range(len(class_cards)):
        card = class_cards[class_cards_index]

        class_card_id = card.get_attribute("id")
        if class_card_id is not None:
            # Within the div element, there is an H2 tag with an ID in the format
            # 'day-title-<day of week>,-<month>-<day of month>'
            xpath = f"//div[@id='{class_card_id}']/ancestor::div[contains(@id, 'day-group-')]"
            container = driver.find_element(By.XPATH, xpath)

            h2_element = container.find_element(By.CSS_SELECTOR, 'h2')

            # day text within the H2 tag is in the format '<day of week (len=3)>, <month (len=3)> <day of month>'
            day = h2_element.text
            day_of_week = get_day_of_week(day)
            if does_date_match(day_of_week, days_of_week) == True:
                if container.get_attribute("id") not in day_div_ids:
                    day_div_ids.append(container.get_attribute("id"))

    return day_div_ids


"""
get all classes starting at 6:00 from the specified div IDs
:param day_container_ids - list of strings containing IDs of divs
:returns list of strings containing IDs of classes that start at 6:00
"""


def find_6pm_class_divs(day_container_ids):
    class_div_ids = []

    for id in day_container_ids:
        day_container = driver.find_element(By.CSS_SELECTOR, f'div[id="{id}"]')
        class_cards = day_container.find_elements(By.CSS_SELECTOR, 'div[id^="class-card-"]')

        for class_card_index in range(len(class_cards)):
            class_card = class_cards[class_card_index]
            class_time = class_card.find_element(By.CSS_SELECTOR, 'p[id^="class-time-"]')

            if "6:00 PM" in class_time.text:
                class_div_ids.append(class_cards[class_card_index].get_attribute("id"))

    return class_div_ids


def exercise_class_name(class_div_id):
    exercise_class_div = driver.find_element(By.CSS_SELECTOR, f'div[id="{class_div_id}"]')
    class_name = exercise_class_div.find_element(By.CSS_SELECTOR, 'h3[id^="class-name-"]')
    return class_name.text


def exercise_date(class_div_id):
    exercise_class_div = driver.find_element(By.CSS_SELECTOR, f'div[id="{class_div_id}"]')
    # the h2 element is not within the exercise div element, but its ancestor div
    xpath = f"//div[@id='{class_div_id}']/ancestor::div"
    ancestor = exercise_class_div.find_elements(By.XPATH, xpath)[-1]

    header_date = ancestor.find_element(By.CSS_SELECTOR, 'h2')
    header_date_text = header_date.text

    if "(" in header_date_text:
        header_date_text = header_date_text[header_date_text.index("(") + 1:header_date_text.index(")")]

    return header_date_text


def book_classes(class_div_ids):
    global new_bookings, already_booked_waitlisted, waitlists_joined, detailed_class_list

    for class_div_id in class_div_ids:
        exercise_class_div = driver.find_element(By.CSS_SELECTOR, f'div[id="{class_div_id}"]')
        book_button = exercise_class_div.find_element(By.CSS_SELECTOR, 'button[id^="book-button-"]')

        class_name = exercise_class_name(class_div_id)
        class_date = exercise_date(class_div_id)

        if book_button.text != "Booked":
            book_button.click()
            print(f"✓ Booked: {class_name} on {class_date}")
            new_bookings += 1

            detailed_class_list.append(
                ClassBookingInfo(
                    name=class_name,
                    date=class_date,
                    time="6:00 PM",
                    waitlisted=False
                )
            )
            # detailed_class_list.append(f"[New Booking] {class_name} on {class_date}")
        elif book_button.text == "Join Waitlist":
            print(f"✓ Joined waitlist for: {class_name} on {class_date}")
            waitlists_joined += 1
            detailed_class_list.append(
                ClassBookingInfo(
                    name=class_name,
                    date=class_date,
                    time="6:00 PM",
                    waitlisted=True
                )
            )
            # detailed_class_list.append(f"[New Waitlist] {class_name} on {class_date}")
        elif book_button.text == "Waitlisted":
            print(f"✓ Already on waitlist: {class_name} on {class_date}")
            already_booked_waitlisted += 1
        elif book_button.text == "Booked":
            print(f"✓ Already booked: {class_name} on {class_date}")
            already_booked_waitlisted += 1


def print_summary():
    global detailed_class_list
    print("\n--- BOOKING SUMMARY ---")
    print(f"Classes booked: {new_bookings}")
    print(f"Waitlists joined: {waitlists_joined}")
    print(f"Already booked/waitlisted: {already_booked_waitlisted}")
    print(
        f"Total Tuesday and Thursday 6pm classes processed: {new_bookings + waitlists_joined + already_booked_waitlisted}")

    if len(detailed_class_list) > 0:
        print("\n--- DETAILED CLASS LIST ---")
        for detail in detailed_class_list:
            message = ''
            if detail.waitlisted:
                message = "[New Waitlist]"
            else:
                message = "[New Booking]"

            message = message + f' {detail.name} on {detail.date}'
            print(message)


"""
verify that the bookings made were completed
"""


def verify_bookings():
    """
    on the bookings page, div ID 'confirmed-bookings-section' contains the confirmed bookings
    within a child div element
    - each booking has an ID starting with 'booking-card-booking_'
    -- class name within h3 tag with an ID starting with 'booking-class-name-booking_'

    div ID 'waitlist-section' contains the confirmed waitlist signups within a child div element
    - each waitlist signup has an ID starting with 'waitlist-card-waitlist_'
    -- class name within h3 tag with an ID starting with 'waitlist-class-name-waitlist_'
    -- class name ends with '(Waitlist)'
    """
    global driver
    driver.get(BOOKING_SUMMARY_URL)

    # verify bookings
    try:
        booked_div = driver.find_element(By.CSS_SELECTOR, '#confirmed-bookings-section')
        booked_items = booked_div.find_elements(By.CSS_SELECTOR, 'div[id^="booking-card-booking_"]')
    except NoSuchElementException:
        # booked classes aren't on the page
        pass

    # verify waitlist signups
    try:
        waitlist_div = driver.find_element(By.CSS_SELECTOR, '#waitlist-section')
        waitlist_items = waitlist_div.find_elements(By.CSS_SELECTOR, 'div[id^="waitlist-card-waitlist_"]')
    except NoSuchElementException:
        # waitlisted classes aren't on the page
        pass

    pass


# --------------------------------------------------------

login()
tuesday_and_thursday_divs = find_day_divs(['tue', 'thu'])
class_divs = find_6pm_class_divs(tuesday_and_thursday_divs)
book_classes(class_divs)
print_summary()
