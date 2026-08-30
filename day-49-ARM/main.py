"""
All of this code is from GitHub Copilot
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the Chrome WebDriver (make sure chromedriver is installed and in PATH)
driver = webdriver.Chrome()

# Open LinkedIn
driver.get("https://www.linkedin.com/jobs")

# Wait for the page to load
time.sleep(3)

# Find the job search input box
search_box = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Search jobs']")

# Enter a job title and submit (example: 'Software Engineer')
search_box.send_keys("Software Engineer")
search_box.send_keys(Keys.RETURN)

# Wait for results to load
time.sleep(5)

# Optionally, print the titles of the first few job postings
job_cards = driver.find_elements(By.CSS_SELECTOR, ".base-search-card__title")
for job in job_cards[:5]:
    print(job.text)

# Close the browser
driver.quit()
