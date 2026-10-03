class ZillowScraper:
    def __init__(self):
        pass

    """
    scrap Zillow search results, getting the price, address, and URL
    """
    def scrape(self):

        pass

    """
    clean up price string by removing '+/mo'
    """
    def cleanup_price(self, price):
        return price.replace('+/mo', '')

    """
    clean up location by removing newlines, pipe symbols, and unnecessary whitespace 
    """
    def cleanup_location(self, location):
        return location.replace('|', ' ').replace('/r', ' ').replace('/n', ' ').strip()
