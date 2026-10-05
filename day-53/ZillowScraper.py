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

        self.search_results = []
        self.zillow_url = os.environ['SOURCE_URL']
        self.google_form_url = os.environ['FORM_LINK']
        pass

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

        load_dotenv()
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
        load_dotenv()



        pass