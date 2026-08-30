from datetime import datetime, timedelta

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

import time


class CookieClickerHandler:
    def __init__(self):
        self.driver = None
        self.chrome_options = None
        self.game_start_time = datetime.now()
        self.current_time = None
        self.purchase_time = None
        self.big_cookie = None
        # commented URL is hosted on CloudFlare and has a CAPTCHA to prove the bot is a human. :)
        # self.url = "https://orteil.dashnet.org/cookieclicker"
        self.url = 'https://ozh.github.io/cookieclicker/'

        # self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_experimental_option("detach", True)
        # self.driver = webdriver.Chrome(self.chrome_options)
        self.PURCHASE_TIME_DELTA = timedelta(seconds=5)
        self.GAME_TIME_DELTA = timedelta(minutes=5)

    def _loop_is_id_present(self, id_to_find, max_attempts=5):
        """
        from https://stackoverflow.com/questions/40029549/how-to-avoid-staleelementreferenceexception-in-selenium-python/41668983#41668983
        :param id_to_find: ID of the element to locate
        :param max_attempts: maximum number of attempts to find the ID
        :return:
        """
        attempt = 1
        while True:
            try:
                return self.driver.find_element(By.ID, value=id_to_find)
            except StaleElementReferenceException:
                if attempt == max_attempts:
                    return None
                else:
                    attempt += 1

    def get_total_cookies(self):
        """
        gets the total number of cookies accumulated
        :return: int representing the total number of cookies
        """
        # will contain text with '<total cookies> cookies'
        print("in get_total_cookies")
        total_cookie_text = self.driver.find_element(By.ID, value="cookies").text
        if total_cookie_text is not None:
            # values over 1000 have a comma in it
            return int(total_cookie_text.split(' ')[0].replace(',', ''))
        else:
            return 0

    def get_cookies_per_second(self):
        """
        gets the number of cookies created per second
        :return: float representing the total number of cookies created per second
        """
        # will contain text with 'per second: <number of cookies per second>'
        print("in get_cookies_per_second")
        print("in get_cookies_per_second")

        attempt = 1
        max_attempts = 10
        cookies_per_second_text = None
        while attempt <= max_attempts and cookies_per_second_text is None:
            try:
                # the stale reference error I'm getting isn't related to finding the element
                # the issue is when I try to get the text from it.
                self.driver.refresh()
                cookies_per_second = self.driver.find_element(By.CSS_SELECTOR, value="#cookiesPerSecond")
                if cookies_per_second is not None:
                    cookies_per_second_text = cookies_per_second.text
            except StaleElementReferenceException:
                if attempt == max_attempts:
                    cookies_per_second_text = None
                    break
                else:
                    attempt += 1

        if cookies_per_second_text is not None:
            # values over 1000 have a comma in it
            return float(cookies_per_second_text.split(' ')[-1].replace(',', ''))
        else:
            return 0

    def click_cookie(self):
        """
        clicks the big cookie
        :return: Nothing
        """
        if self.big_cookie is None:
            self.big_cookie = self.driver.find_element(By.ID, value="bigCookie")

        if self.big_cookie is not None:
            self.big_cookie.click()

    def click_golden_cookie(self):
        """
        click the golden cookie if present
        :return:
        """
        print("in click_golden_cookie")
        golden_cookie = self.driver.find_element(By.ID, value="goldenCookie")
        if golden_cookie is not None:
            golden_cookie.click()

    def select_language(self):
        """
        click the English language option on the language selector
        :return: True if a language was selected, False if not
        """
        # give the page a chance to load
        # time.sleep(20)

        print("in select_language")

        check_start_time = datetime.now()
        current_time = datetime.now()
        check_duration = timedelta(seconds=5)
        language_clicked = False

        while current_time - check_start_time <= check_duration or language_clicked == False:
            try:
                # language selection div found - click on the English selection
                language_en = self.driver.find_element(By.ID, value='langSelect-EN')
                if language_en is not None:
                    try:
                        language_en.click()
                        language_clicked = True
                    except selenium.common.exceptions.StaleElementReferenceException:
                        pass
            except selenium.common.exceptions.NoSuchElementException:
                pass
            finally:
                current_time = datetime.now()

        if language_clicked:
            return True
        else:
            return False

    def find_products(self, total_cookies):
        """
        locate products the player can purchase
        :param total_cookies: number of cookies the player has
        :return: ID of the product div that is the most expensive product the player can buy, or
            None if the player can't afford any products
        """
        """
		- search for div elements with a class of 'product' that don't have
		  a class of 'locked' and don't have a class of 'disabled'
			- product price is in a span with an ID of 'productPrice<index>'
			  and a class of 'price'
		- build a dictionary of purchasable products
			- key of div ID
			- value of price
		- return the key (element ID) with the highest price
        """
        buyable_products = self.driver.find_elements(By.CSS_SELECTOR, value='div.product.enabled')
        if buyable_products is None or len(buyable_products) == 0:
            return None
        else:
            # at least one product can be purchased
            # build a dictionary with the key being the ID of the product div and the value
            #  of the product's price
            # while upgrades appear to be sorted by price, products are sorted by the number of cookies
            #   generated
            products = {}
            for i in range(len(buyable_products)):
                product_id = buyable_products[i].get_attribute("id")
                # prices over 1000 have a comma...
                price = int(buyable_products[i].find_element(By.CSS_SELECTOR, value='span.price')
                            .text
                            .replace(',', ''))

                if price <= total_cookies:
                    products[product_id] = price

            # sort the prices in descending order - highest price is first
            sorted_products = sorted(products.items(), key=lambda item: item[1], reverse=True)
            sorted_products_dict = dict(sorted_products)

            # get the names of the keys, return the first one
            # have to convert to list to access a key by index value
            keys = list(sorted_products_dict.keys())
            return keys[0]

    def find_upgrades(self):
        """
        locate upgrades the player can purchase
        :return: ID of the element containing the most expensive upgrade, None if one wasn't found
        """
        buyable_upgrades = self.driver.find_elements(By.CSS_SELECTOR, value="#upgrades div.enabled")
        if buyable_upgrades is None or len(buyable_upgrades) == 0:
            return None
        else:
            # at least one upgrade can be purchased
            # build a list of the IDs that are enabled
            upgrades = []
            for i in range(len(buyable_upgrades)):
                upgrade_id = buyable_upgrades[i].get_attribute("id")
                upgrades.append(upgrade_id)

            return upgrades[-1]

    def accept_banner(self):
        """
        clicks the "got it!" button on the banner that appears on the bottom of the page
        :return:
        """
        print("in accept_banner")
        try:
            banner = self.driver.find_element(By.CSS_SELECTOR, value='div.cc_container--open')
            if banner is not None:
                # got_it_button = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/a[1]')
                got_it_button = banner.find_element(By.CSS_SELECTOR, value='a.cc_btn_accept_all')
                got_it_button.click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def play_game(self):
        """
        plays the cookie clicker game
        :return: cookies per second after 5 minutes
        """
        """
        - CALL select_language
		- set current_time to current date/time
		- set purchase_time to current date/time
		- while difference between current_time and game_start_time is less than 5 minutes
			- while difference between purchase_time and current_time is less than 5 seconds
				- CALL click cookie
				- set current_time to current date/time
				
			- CALL get_total_cookies
			- CALL find_products
				- if something returned get the element with an ID
				  matching the result and click it
			
			- set purchase_time to current date/time
		- CALL get_cookies_per_second
		- return number of cookies per second
        """

        print("Preparing Selenium")
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(self.chrome_options)
        self.driver.get(self.url)
        self.driver.maximize_window()

        print(f"game start time: {self.game_start_time}")

        print("Selecting a language")
        self.select_language()
        self.current_time = datetime.now()
        self.purchase_time = datetime.now()

        self.accept_banner()

        # ----- commented for debugging
        print("In outer game loop")
        # while the difference between the game start time and the current time is less than 5 minutes
        while (self.current_time - self.game_start_time) < self.GAME_TIME_DELTA:

            self.click_cookie()
            # self.click_golden_cookie()

            # once the time delta between the current time and the purchase time exceeds
            # the purchase time delta, get the total cookies and look for the most
            # expensive product and upgrade
            if (self.current_time - self.purchase_time) > self.PURCHASE_TIME_DELTA:
                cookies = self.get_total_cookies()

                # look for the most expensive product and upgrade that can be purchased
                # if a product and upgrade are returned the upgrade gets priority
                product_id = self.find_products(total_cookies=cookies)
                # upgrade_id = self.find_upgrades()

                print(f"product ID: {product_id}")
                # print(f"upgrade ID: {upgrade_id}")

                # if upgrade_id is not None:
                #     # upgrade div ID was returned, find the element and click on it
                #     upgrade_div = self.driver.find_element(By.CSS_SELECTOR, value=f"#{upgrade_id}")
                #     upgrade_div.click()
                # elif product_id is not None:
                if product_id is not None:
                    # product div ID was returned, find the element and click on it
                    product_div = self.driver.find_element(By.CSS_SELECTOR, value=f"#{product_id}")
                    product_div.click()

                # now that the chance to purchase a product has been passed, time
                # to update purchase_time
                self.purchase_time = datetime.now()

            # print("In inner game loop")
            # # while the difference between the purchase time and the current time is less than 5 seconds
            # # AND the current time is less than the game time delta
            # while ((self.current_time - self.purchase_time) < self.PURCHASE_TIME_DELTA and
            #        (self.current_time - self.game_start_time) < self.GAME_TIME_DELTA):
            #    self.click_cookie()
            #    self.current_time = datetime.now()
            #
            # # 5 seconds have elapsed, get the total cookies and see if a product can be purchased
            # cookies = self.get_total_cookies()
            # product_id = self.find_products(total_cookies=cookies)
            # upgrade_id = self.find_upgrades()
            #
            # print(f"product ID: {product_id}")
            # print(f"upgrade ID: {upgrade_id}")
            #
            # if upgrade_id is not None:
            #     # upgrade div ID was returned, find the element and click on it
            #     upgrade_div = self.driver.find_element(By.CSS_SELECTOR, value=f"#{upgrade_id}")
            #     upgrade_div.click()
            # elif product_id is not None:
            #     # product div ID was returned, find the element and click on it
            #     # product_div = self.driver.find_element(By.ID, value=product_id)
            #     product_div = self.driver.find_element(By.CSS_SELECTOR, value=f"#{product_id}")
            #     product_div.click()
            #
            # # now that the chance to purchase a product has been passed, time
            # # to update purchase_time
            # self.purchase_time = datetime.now()

            # update the current time
            self.current_time = datetime.now()

        # the game time duration has elapsed
        # wait a few seconds, then get the number of cookies per second
        # time.sleep(5)
        # cookies_per_second = self.get_cookies_per_second()
        try:
            cookies_per_second_element = self.driver.find_element(By.ID, value="cookiesPerSecond")
            cookies_per_second = cookies_per_second_element.text
        except StaleElementReferenceException:
            cookies_per_second = "Couldn't get cookies per second"

        self.driver.quit()

        # game over - get the cookies per second and return it
        return cookies_per_second
