from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# from the site https://en.wikipedia.org/wiki/Main_Page
# get the total article count and print it
URL = "https://en.wikipedia.org/wiki/Main_Page"

# keep Chrome open after program finished
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
driver.maximize_window()

# total article count is within a div element with the id 'articlecount'
# contained within an anchor tag with the title 'Special:Statistics"
total_articles = driver.find_element(By.CSS_SELECTOR, value='#articlecount li:last-child a')
print(total_articles.text)
# total_articles.click()

# find element by link text
all_portals = driver.find_element(By.LINK_TEXT, value='Content portals')
# all_portals.click()

# find the "Search" <input> by Name
search = driver.find_element(By.NAME, value='search')
search.send_keys("Python")
search.send_keys(Keys.ENTER)

# # closes a single tab
# driver.close()
# # closes the entire browser program
# driver.quit()