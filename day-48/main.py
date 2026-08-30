from selenium import webdriver
from selenium.webdriver.common.by import By
import pprint

# URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
URL = "https://www.python.org"
# keep Chrome open after program finished

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
#
# # when I run the program, a page with a button appears to 'Continue Shopping'.
# # it is a button element with a class of 'a-button-text'
# continue_button = driver.find_element(By.CLASS_NAME, 'a-button-text')
# continue_button.click()
#
# # get hold of the price
# # dollars and decimal point in span.a-price-while
# # cents in span.a-price-fraction
# price_dollar = driver.find_element(By.CLASS_NAME, "a-price-whole").text
# price_cents = driver.find_element(By.CLASS_NAME, "a-price-fraction").text
# print(f"The price is {price_dollar}.{price_cents}")

# search_input = driver.find_element(By.NAME, value='q')
# print(search_input.tag_name)
# print(search_input.get_attribute("placeholder"))
#
# submit_button = driver.find_element(By.ID, value='submit')
# # submit_button.click()
# print(submit_button.size)
#
# doc_link = driver.find_element(By.CSS_SELECTOR, value='.documentation-widget a')
# print(doc_link.text)
# print(doc_link.get_attribute('href'))
#
# submit_bug_link = driver.find_element(By.XPATH, value='/html/body/div/footer/div[2]/div/ul/li[3]/a')
# print(submit_bug_link.get_attribute('href'))
#
# anchor_tags = driver.find_elements(By.CSS_SELECTOR, value='a')

# lecture 347 challenge
# build a nested dictionary
# - key is index number
# - value is a dictionary with time and name keys

# this gets the month and day
event_times = driver.find_elements(By.CSS_SELECTOR, value='.event-widget time')
# this gets the event links
event_names = driver.find_elements(By.CSS_SELECTOR, value='.event-widget time + a')

# for event in event_times:
#      print(event.text)
#
# for event in event_names:
#     print(event.text)

event_data = {}
for i in range(len(event_times)):
    event_data[i] = {'time': event_times[i].get_attribute('datetime').split('T')[0], 'name': event_names[i].text}
    # event_data.update({
    #     i: {'time': event_times[i].get_attribute('datetime').split('T')[0], 'name': event_names[i].text},
    # })

# print(event_data)
pprint.pp(event_data)
# # closes a single tab
# driver.close()
# # closes the entire browser program
driver.quit()
