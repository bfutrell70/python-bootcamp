import selenium.common
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# the goal of the lesson for day 50 is to log into LinkedIn,
# search for a job and apply for it.
#
# Since I'm perfectly happy with my job and using Selenium on
# LinkedIn violates their terms of use, I'm trying something
# different.
#
# Instead, I'll be using Selenium to access stayonline.com -
# the website of my former employer. Their robots.txt file
# does not mention Selenium, only disallowing bots indexing
# specific paths.

"""
Some items of interest:
#u_search_text - search field on top of the page
    - the site will let you search without any search text, which basically
      returns all products.
#u_search_submit - button to search for the text in the search field above
    - appears to be triggered if Enter is pressed in #u_search_text
a.header__prodcat-toggle - shop all products toggle
    div.prodcat-flyout-fullwidth - dropdown showing all product categories
        - display is set to 'none' if the dropdown isn't shown
#five-tiles - div containing 5 tiles representing different product categories  
    - a[1] - anchor tag with an href of 'nema-power-cords'
a data-key='321F7088665842E5BEFFE23D32742982' - anchor tag for 
    NEMA Straight Blade Power Cords
    URL of category/c-name-straight-blade-cords.asp
a data-key='EB2661C642B04FF29043F2FB2C6916AE' - anchor tag for
    NEMA 5-15 to C13 Power Cords page
    URL of category/c-nema-5-15-to-c13-color-cords.asp
#input_ColorGreen - input checkbox to search for green cords
#input_CableLength12E8Meter2F6Feet - input checkbox to search for cords with a length of 1.8 meter/6 feet
button with class 'prod-card__atc btn btn-primary btn-cart-add' - button to add a product to cart
button with class 'btn btn btn-primary dropdown-toggle' 
    - beside above button
    - dropdown options to add to favorites and add to quote
        - anchor tag with class 'global-modal', href starting with 'add_product_to_favorites.asp'
        - anchor tag with data-bind value of 'click: addToSavedCart'
input.qty-input
    - quantity for a product
    - if the item is in stock, there will be values for the min and max attributes

#header__cart-preview
    - unordered list containing the My Cart button
    *** li.link-parent.drop
        - list item containing the anchor tag that displays the cart preview 
        - 'open' class added to the list item if the cart preview is open
    *** a.header__cart-preview__toggle
        - anchor tag that toggles showing and hiding the cart preview

a.btn.btn-block.btn-primary.view-cart-button
    - anchor tag with an href starting with '/showcart.asp'
    - full shopping cart page
    
a.btn.btn-block.estimate-shipping-button.global-modal
    - anchor tag with an href of 'shipping_estimator.asp'

#global_modal
    - modal dialog containing the Estimate Shipping tool
    - if hidden aria-hidden attribute will be 'true'
    - if visible aria-hidden attribute will be 'false' and an additional class of 'in' is present
    
(just in case clicks are intercepted when clicking on a product)
div.t-consentPrompt
    - div on the bottom of the window displaying cookie preferences
    - button.t-acceptAllButton
        - Accept All cookies button

** in minicart
a.close.text-danger (there is an ID but not human-readable)
    - remove from cart link
    - displays a confirmation dialog, so I don't know if Selenium can handle clicking that

** on showcart.asp
button.btn-primary type="submit" - Checkout as Guest button

Task to perform:
- open the https://www.stayonline.com site, find some cords and add them to a quote.        
- either navigate through the product categories, or search for cords.
- there may be a chance that searching for something may not return results.
"""

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Set up the Chrome WebDriver (make sure chromedriver is installed and in PATH)
driver = webdriver.Chrome(chrome_options)

# Open StayOnline's website
driver.get("https://www.stayonline.com/")

# click the accept all cookies button
try:
    accept_cookies_button = driver.find_element(By.CSS_SELECTOR, "button.t-acceptAllButton")
    accept_cookies_button.click()
except selenium.common.exceptions.NoSuchElementException:
    pass

# find a NEMA 5-15 to C13 power cord
print("Searching for '5-15 to C13 yellow'")
search_input = driver.find_element(By.ID, "u_search_text")
search_input.send_keys("5-15 to C13 yellow")

# click the search button
print("clicking the search submit button")
search_button = driver.find_element(By.ID, "u_search_submit")
search_button.click()

# wait for the page to load
time.sleep(5)

# locate skus on the page (as of 8/14/2025, the first two skus are in stock - 2308 and 2073)
# div.prod-card is a div containing all markup for a product
print("searching for all product cards on the page")
cords = driver.find_elements(By.CSS_SELECTOR, "div.prod-card")

if cords and len(cords) > 0:
    for cord in cords:
        # look for markup that indicates that the product is in stock
        # custom molded cords lack this markup
        try:
            print("searching for the 'add-on' anchor tag")
            in_stock = cord.find_element(By.CSS_SELECTOR, "a.add-on")

            if in_stock:
                print("product in stock, now searching for the quantity input")

                # cord is in stock
                # find the quantity input
                qty_input = cord.find_element(By.CSS_SELECTOR, "input.qty-input")

                # delete the contents of the field first since it contains '1' by default
                time.sleep(2)
                qty_input.send_keys(Keys.ARROW_LEFT)
                qty_input.send_keys(Keys.DELETE)
                qty_input.send_keys("2")

                # find the add to cart button
                print("finding the add to cart button")
                add_to_cart = cord.find_element(By.CSS_SELECTOR, "button.btn-cart-add")
                add_to_cart.click()

                time.sleep(5)
        except selenium.common.exceptions.NoSuchElementException:
            # couldn't find the add-on anchor tag so the product is a custom-made cord
            pass

    time.sleep(5)

    # done adding items to cart - go the shopping cart page
    print("searching for the cart preview anchor tag")
    my_cart_toggle = driver.find_element(By.CSS_SELECTOR, "a.header__cart-preview__toggle")
    my_cart_toggle.click()

    time.sleep(5)

    print("searching for the view cart button")
    view_cart_button = driver.find_element(By.CSS_SELECTOR, "a.view-cart-button")
    view_cart_button.click()

    time.sleep(5)

    # checkout!
    # button.btn-primary type="submit" - Checkout as Guest button
    print("searching for the checkout as guest button")
    checkout_button = driver.find_element(By.XPATH, "//*[@id='frmGuest']/button")
    print(f"checkout button text: {checkout_button.text}")
    checkout_button.click()

    time.sleep(5)

    # fill in the order contact, bill to contact information
    # set Shipping same as billing
    """
    - entire form on the checkout page has an ID of 'form_builder'
        each section is in a div element
        - billing section has an ID of 'billing-container'
            - email field has an ID of 'c_em'
            - first name has an ID of 'c_f_nm'
            - last name has an ID of 'c_l_nm'
            - phone has an ID of 'c_phone'
            
            - company name has an ID of 'nm'
            - street address has an ID of 'address'
            - street address 2 has an ID of 'address2'
            - country dropdown has an ID of 'c_country'
            - city has an ID of 'c_city'
            - state/province dropdown has an ID of 'select_c_state'
            - zip/postal code has an ID of 'c_zip'
            
        - checkbox to set shipping the same as billing ID is 'setsame'
        - by default the ship to residential address is checked
        - shipping contact phone has an ID of 's_phone'
        - shipping email address has an ID of 'em'
        - shipping name/company name is required
            - has an ID of 's_company'
            
        - Save and Proceed button has an ID of 'btnProceed'
    """
    # fill in contact information
    print("searching for the contact email input")
    contact_email = driver.find_element(By.ID, "c_em")
    contact_email.send_keys("johndoe@gmail.com")

    print("searching for the contact first name input")
    contact_first_name = driver.find_element(By.ID, "c_f_nm")
    contact_first_name.send_keys("John")

    print("searching for the contact last name input")
    contact_last_name = driver.find_element(By.ID, "c_l_nm")
    contact_last_name.send_keys("Doe")

    time.sleep(2)

    # the phone number field automatically adds dashes to the appropriate locations,
    # no need to type them in
    # 2025-08-25 - for some reason the contact phone field is not being populated
    #   if I run 'contact_phone.send_keys("1234567890")' from the console when debugging it works
    # contact_phone = driver.find_element(By.ID, "c_phone")
    print("searching for the contact phone input")
    contact_phone = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/form/div[2]/fieldset[1]/div/div[4]/div[2]/input')
    time.sleep(0.5)
    contact_phone.send_keys("1234567890")

    print(f"contact phone text: {contact_phone.text}")

    # fill in company name and address
    print("searching for the company name input")
    company_name = driver.find_element(By.ID, "nm")
    company_name.send_keys("Widgets R Us")

    print("searching for the street address input")
    street_address = driver.find_element(By.ID, "address")
    street_address.send_keys("2633 Pleasant Hill Dr.")

    print("searching for the street address 2 input")
    street_address2 = driver.find_element(By.ID, "address2")
    street_address2.send_keys("Lot 102")

    print("searching for the city input")
    city = driver.find_element(By.ID, "c_city")
    city.send_keys("Zebulon")

    # country defaults to 'United States', so this shouldn't need to
    # be changed

    print("searching for the state/province input")
    state_province  = driver.find_element(By.ID, "select_c_state")
    state_province.send_keys("nnnnnnn" + Keys.ENTER) # North Carolina is the 7th state starting with 'N'

    print("searching for the Zip Code/postal code input")
    zip_code = driver.find_element(By.ID, "c_zip")
    zip_code.send_keys("27597")

    print("searching for the shipping same as billing checkbox")
    shipping_same = driver.find_element(By.ID, "setsame")
    shipping_same.click()

    # print("searching for the shipping company input")
    # shipping_company_name = driver.find_element(By.ID, "s_company")
    # shipping_company_name.send_keys("Widgets R Us")

    print("searching for the proceed button")
    save_and_proceed_button = driver.find_element(By.ID, "btnProceed")
    save_and_proceed_button.click()

