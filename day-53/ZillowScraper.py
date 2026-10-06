import time

import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from result_data import *

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class ZillowScraper:
    def __init__(self):
        load_dotenv()

        self.search_results: list[ResultData] = []
        self.zillow_url = os.environ['SOURCE_URL']
        self.google_form_url = os.environ['FORM_LINK']
        self.google_form_response_url = os.environ['FORM_RESPONSE_LINK']

        chrome_options = webdriver.ChromeOptions()
        # if True must close Chrome manually before the script is re-run
        chrome_options.add_experimental_option("detach", True)

        # have Selenium create its own user profile
        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")

        # tell the Chrome driver to use the user data directory specified above
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

        self.driver = webdriver.Chrome(chrome_options)


    """
    scrap Zillow search results, getting the price, address, and URL
    """
    def scrape(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Priority": "u=0, i",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
        }

        response = requests.get(self.zillow_url, headers=headers)
        page_data = response.text

        soup = BeautifulSoup(markup=page_data, features='html.parser')

        results = soup.select('.StyledPropertyCardDataWrapper')

        print(len(results))

        for result in results:
            url = result.select_one('.StyledPropertyCardDataArea-anchor').attrs['href']
            price = self.cleanup_price(result.select_one('.PropertyCardWrapper__StyledPriceLine').text)
            address = self.cleanup_location(result.select_one('address').text)

            print(f"price: {price}, address: {address}, url: {url}")

            search_result = ResultData(price, address, url)
            self.search_results.append(search_result)

        pass

    """
    clean up price string by removing '+/mo'
    """
    def cleanup_price(self, price):
        result = int(price.replace('+', '').replace('/mo', '').replace('1bd', '').replace('1 bd', '').replace('$', '').replace(',', '').strip())
        formatted_result = f"${result:,}"
        return formatted_result

    """
    clean up location by removing newlines, pipe symbols, and unnecessary whitespace 
    """
    def cleanup_location(self, location):
        result = location.replace('|', ' ').replace('/r', ' ').replace('/n', ' ').strip()
        result = " ".join(result.split())
        return result


    """
    add data scraped from Zillow search results to a Google Form
    """
    def add_data_to_google_form(self):
        wait = WebDriverWait(self.driver, 2)

        # form inputs all have the classes 'whsOnd' and 'zHQkBf'
        # If I search for all inputs with these classes I should get three results
        # submit button is a div[aria-label='Submit']

        index = 0
        search_result_count = len(self.search_results)

        # input order is address, price, link
        for search_result in self.search_results:
            # navigate to the Google Forms page
            self.driver.get(self.google_form_url)
            time.sleep(2)
            print(f"working on result index {index + 1} of {search_result_count}")

            ec.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))

            input_fields = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')

            input_fields[0].send_keys(search_result.location)
            input_fields[1].send_keys(search_result.price)
            input_fields[2].send_keys(search_result.link)

            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Submit"]')
            submit_button.click()

            # now on the formResponse page
            # self.driver.get(self.google_form_response_url)
            # time.sleep(1)
            # print(self.driver.current_url)

            ec.presence_of_element_located((By.CSS_SELECTOR, 'a[href$="usp=form_confirm"'))
            submit_another_response_link = self.driver.find_element(By.CSS_SELECTOR, 'a[href$="usp=form_confirm"')
            submit_another_response_link.click()
            time.sleep(2)

            index += 1

    def export_search_results(self):
        # Need to log into Google to export the results entered into the Google Form.
        # Unable to log in on the "awnc_guest" Wi-Fi network or in a VM on the corporate network.
        # Will try this at home and see if I have the same issues.
        pass