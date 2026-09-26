import os
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

TINDOG_URL = 'https://app.100daysofpython.dev/services/tindog/u/ttoIBC8MQaOqUfSEEIRgL7zOLSuFxVpm'
ACCOUNT_EMAIL = 'bfutrel@gmail.com'
ACCOUNT_PASSWORD = 'Python99!'

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

driver.get(TINDOG_URL)
time.sleep(2)

# step 2 - navigate to login page
def login():
    driver.find_element(By.CSS_SELECTOR, ".btn-tindog-login").click()
    time.sleep(0.5)

    # modal displayed, select 'Login with FACEBARK'
    try:
        driver.find_element(By.CSS_SELECTOR, ".btn-facebark").click()
        time.sleep(0.5)

        # --- step 2 is concerned with navigating to the login page
        # a separate window will display with the FACEBARK login
        base_window = driver.window_handles[0]
        fb_login_window = driver.window_handles[1]
        driver.switch_to.window(fb_login_window)
        print(driver.title)

        facebark_login_card = driver.find_element(By.XPATH, "/html/body/div[2]/div")

        facebark_email = facebark_login_card.find_element(By.ID, 'email')
        facebark_email.send_keys(ACCOUNT_EMAIL)

        facebark_password = facebark_login_card.find_element(By.ID, 'pass')
        facebark_password.send_keys(ACCOUNT_PASSWORD)
        facebark_password.send_keys(Keys.ENTER)

        time.sleep(0.5)

        driver.switch_to.window(base_window)
        print(driver.title)
    except NoSuchElementException:
        print('no element found!')
        return False

def dismiss_popups():
    # dismiss location popup (allow)
    driver.find_element(By.XPATH, "/html/body/main/div/div/form/button").click()
    time.sleep(0.5)

    # dismiss notification popup (not interested)
    driver.find_element(By.XPATH, "/html/body/main/div/div/form/button[2]").click()
    time.sleep(0.5)

    # dismiss cookies popup (accept)
    driver.find_element(By.XPATH, '/html/body/main/div/div/form/button').click()
    time.sleep(0.5)

    pass

# ----------------------------------------
login()
dismiss_popups()

