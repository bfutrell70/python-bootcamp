from ZillowScraper import *

"""
using Zillow to research house prices that fit a particular criteria for a client
transfer data into a form, which will create a sheet in Google Sheets

BeautifulSoup and Selenium

BeautifulSoup was covered in Section 45 - Intermediate+ Web Scraping with BeautifulSoup

find all places they can rent in San Francisco
- up to $3,000 per month
- has to have at least one bedroom
- expensive, hard to find locations

use clone of Zillow site
https://appbrewery.github.io/Zillow-Clone

using BeautifulSoup to scrape the results
- get the following data:
    - price
    - address
    - URL that the result is linked to

once the data is retrieved, use Selenium to autofill in a Google Form
    one form per search result
    option to create a Google Sheet from the form data
"""
zillow_scraper = ZillowScraper()
zillow_scraper.scrape()
zillow_scraper.add_data_to_google_form()