from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

URL = "https://secure-retreat-92358.herokuapp.com/"

# keep Chrome open after program finished
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
driver.maximize_window()

# enter First Name, Last Name, and Email address
# then click Sign Up button

# find elements on page
first_name_input = driver.find_element(By.NAME, value='fName')
last_name_input = driver.find_element(By.NAME, value='lName')
email_input =  driver.find_element(By.NAME, value='email')
submit_button = driver.find_element(By.CSS_SELECTOR, value='button[type="submit"]')

# add text to input elements
first_name_input.send_keys('Test')
last_name_input.send_keys('User')
email_input.send_keys('testuser@example.com')

# submit the form
submit_button.click()

# giving the user a chance to look at the results
time.sleep(15)

# # closes a single tab
# driver.close()
# # closes the entire browser program
driver.quit()