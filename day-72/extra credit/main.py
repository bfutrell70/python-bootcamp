from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas

"""
- scrape data from PayScale's website for pay scale information by college major
- may need to use archive.org's Wayback Machine to get updated data
- https://web.archive.org/web/20170927161827/https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors?page=33
	- button to see full list
		- anchor tag with classes 'btn', 'btn-primary', 'btn-block'
		- text "See Full List"
		- find and click this button to see the full list of majors
	- data within div element with an ID of 'collegeSalaryReportContent'
		- table elememt with classes of 'table', 'table-bordered', 'table-striped', 'table-condensed'
		- table rows have an ID of 'datatable-<row number>', with <row-number> starting at 0
		- table data within each table cell is stored within a span element
		- columns:
			- Rank (most are numbers, but some have '<rank> (tie)'
			- Major
			- Degree Type
			- Early Career Pay
			- Mid-Career Pay
			- % High Meaning
"""

SOURCE_URI = "https://web.archive.org/web/20170927161827/https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors?page=33"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(SOURCE_URI)

report_content = driver.find_element(By.CSS_SELECTOR, "#collegeSalaryReportContent")
content_row = report_content.find_elements(By.CSS_SELECTOR, ".row .row")[-1]

full_list_button = content_row.find_element(By.CSS_SELECTOR, "a.btn-block")
full_list_button.click()

data_table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
print(len(data_table_rows))

for row in data_table_rows:
    # first row is column headings
    pass