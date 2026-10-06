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

FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdqyOPYxw_6CEKBG032E6qTp7m7RuwcBeuME9YIWPEuPqHoxg/viewform?usp=dialog"

"""
search result markup

Search results are contained within an unordered list
    - each list item represents a single search result
        - li.ListItem-c11n-8-84-3-StyledListCardWrapper
    - in each list item is an article element that contains the data
        - data is contained in div.StyledPropertyCardDataWrapper
            - price:                                span.PropertyCardWrapper__StyledPriceLine
            - address:                              address element, data-test attribute of 'property-card-addr'
            - URL that the result is linked to:     a.StyledPropertyCardDataArea-anchor
            
    - after getting the data:
        - clean up the price to remove "+/mo"
        - clean up addresses - remove newlines, pipe symbols, and unnecessary whitespace 
"""

zillow_scraper = ZillowScraper()
zillow_scraper.scrape()
zillow_scraper.add_data_to_google_form()