from selenium import webdriver
import time

from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class InstaFollower:
    def __init__(self):
        self.USERNAME = 'bfutrel@gmail.com'
        self.PASSWORD = 'yPPSy99K4eEq4lfQ'
        self.SIMILAR_ACCOUNT = 'rordongamsay'
        self.PROFILE_NAME = '@bfutrel'
        self.BASE_URL = 'https://app.100daysofpython.dev/services/share-a-naan'
        self.WELCOME_URL = f'{self.BASE_URL}/welcome'
        self.FOLLOWERS_URL = f'{self.BASE_URL}/u/{self.SIMILAR_ACCOUNT}/followers'

        chrome_options = webdriver.ChromeOptions()
        # if True must close Chrome manually before the script is re-run
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(chrome_options)

    def login(self):
        wait = WebDriverWait(self.driver, 2)
        self.driver.get(self.BASE_URL)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))

        """
        login fields are in a div shown on the right of the page
            input[name='username']
            input[name='password']
            press enter after entering the password
        
        save your login info popup
            div id "popup-save-login"
               div.naan-popup-dismiss, text "Not now"
                   click it
            
        turn on notifications popup
            div id "popup-notifications"
               button.naan-popup-dismiss, text "Not Now"
                   click it
        """

        username_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        username_input.send_keys(self.USERNAME)

        password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        password_input.send_keys(self.PASSWORD)
        password_input.send_keys(Keys.RETURN)

        time.sleep(1)

        dismiss_save_login_popup = self.driver.find_element(By.CSS_SELECTOR, 'div.naan-popup-dismiss')
        dismiss_save_login_popup.click()
        time.sleep(1)

        dismiss_notifications_popup = self.driver.find_element(By.CSS_SELECTOR, 'button.naan-popup-dismiss')
        dismiss_notifications_popup.click()
        time.sleep(1)

    def find_followers(self):
        """
        NOTE: None of the accounts at the top of the page have any followers - you must click Search,
        search for one of the three accounts mentioned in the Manage Share-a-Naan page, then press
        enter.

        button with an attribute of "data-naan-search-toggle"
            click it

        input.naan-search-input
            enter one of the three account names from the Manage Share-a-Naan page
            press enter

        anchor tag with class of "naan-followers-link"
            click it

            new URL appears - https://app.100daysofpython.dev/services/share-a-naan/u/rordongamsay/followers
            load the new page in WebDriver

        Followers page
            each follower is in a div element with the class 'naan-follower-row'
                call the follow method, passing in the div element

        """
        self.driver.get(self.FOLLOWERS_URL)
        followers = self.driver.find_elements(By.CSS_SELECTOR, 'div.naan-follower-row')

        return followers

    def follow(self, follower):
        """
        passing in the div representing the follower
        find the button without the class 'is-following'
        if it is found click on it
        """
        try:
            follow_button = follower.find_element(By.CSS_SELECTOR, 'div:not(.is-following)')

            follow_button.click()
        except NoSuchElementException:
            pass
