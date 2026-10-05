import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class InternetSpeedTwitterBot:
    def __init__(self, promised_down = 500, promised_up = 500):
        self.down: float = 0.0
        self.up: float = 0.0
        # NOTE: This site is blocked by the firewall on the "awnc_guest" Wi-Fi network
        self.SPEEDTEST_URL = "https://www.speedtest.net"
        self.Y_URL = 'https://app.100daysofpython.dev/services/y/login'
        self.Y_EMAIL_ADDRESS = 'bfutrel@gmail.com'
        self.Y_PASSWORD = 'X-QdVDC1C1j-TPKo'
        self.PROMISED_DOWN = promised_down
        self.PROMISED_UP = promised_up

        chrome_options = webdriver.ChromeOptions()
        # if True must close Chrome manually before the script is re-run
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(chrome_options)

    def get_internet_speed(self):
        self.driver.get(self.SPEEDTEST_URL)
        time.sleep(2)


    def tweet_at_provider(self):
        wait = WebDriverWait(self.driver, 2)

        self.driver.get(self.Y_URL)
        time.sleep(2)

        # login_link = self.driver.find_element(By.CSS_SELECTOR, "a.y-login-link")
        # login_link.click()
        #
        # time.sleep(2)
        email = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        email.send_keys(self.Y_EMAIL_ADDRESS)
        password = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password.send_keys(self.Y_PASSWORD)
        password.send_keys(Keys.RETURN)

        # submit = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        # submit.click()

        time.sleep(3)

        # post_button = self.driver.find_element(By.CSS_SELECTOR, "#post-btn")
        # post_button.click()

        message = (f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for "
                   f"{self.PROMISED_DOWN}down/{self.PROMISED_UP}up?")

        wait.until(ec.presence_of_element_located((By.ID, "tweet-compose")))

        # compose = self.driver.find_element(By.CSS_SELECTOR, "#tweet-compose")
        compose = self.driver.find_element(By.CSS_SELECTOR, "div[aria-label='Post text']")
        compose.send_keys(message)

        post_button = self.driver.find_element(By.CSS_SELECTOR, "#post-btn")
        post_button.click()