import os
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

TINDOG_URL = 'https://app.100daysofpython.dev/services/tindog/u/ttoIBC8MQaOqUfSEEIRgL7zOLSuFxVpm'
ACCOUNT_EMAIL = 'bfutrel@gmail.com'
ACCOUNT_PASSWORD = 'Python88!'

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

# step 2 - navigate to login page
def login():
    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn-tindog-login")
    login_button.click()
    time.sleep(0.5)

    # modal displayed, select 'Login with FACEBARK'
    try:
        modal_dialog = driver.find_element(By.CSS_SELECTOR, "div.show")
        login_with_facebark = modal_dialog.find_element(By.CSS_SELECTOR, "button.btn-facebark")
        login_with_facebark.click()
        time.sleep(0.5)

        # a separate window will display with the FACEBARK login
        # use XPATH to locate the login card
        # facebark_login_card = driver.find_element(By.XPATH, "/html/body/div[2]/div")
        #
        # facebark_email = facebark_login_card.find_element(By.ID, 'email')
        # facebark_email.clear()
        # facebark_email.send_keys(ACCOUNT_EMAIL)
        #
        # facebark_password = facebark_login_card.find_element(By.ID, 'password')
        # facebark_password.clear()
        # facebark_password.send_keys(ACCOUNT_PASSWORD)
        #
        # facebark_login = facebark_login_card.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        # facebark_login.click()
        # time.sleep(0.5)
    except NoSuchElementException:
        print('no element found!')
        return False


# ----------------------------------------
login()


