import os

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

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

"""
test JavaScript code I wrote to get table rows within the table element without
getting the rows withn the subtables contained within the ending table cell
---------
const report_div = document.getElementById("collegeSalaryReportContent");
console.log(report_div);

const data_table = report_div.querySelector(".row .row table");
console.log(data_table);

const table_body_rows = data_table.querySelectorAll('tr[id]');
console.log(table_body_rows);
"""

report_content = driver.find_element(By.CSS_SELECTOR, "#collegeSalaryReportContent")
content_row = report_content.find_elements(By.CSS_SELECTOR, ".row .row")[-1]

print('clicking See Full List button')
full_list_button = content_row.find_element(By.CSS_SELECTOR, "a.btn-block")
full_list_button.click()

print("getting data rows from table")
data_table_rows = report_content.find_elements(By.CSS_SELECTOR, "table tbody tr[id]")
print(f'data rows found: {len(data_table_rows)}')

# set up an empty DataFrame with column names
salary_data = pd.DataFrame(columns=['rank', 'major', 'degree_type', 'early_career_pay', 'min_career_pay', 'percent_high_meaning']).astype({
	'rank': 'string', 
	'major': 'string', 
	'degree_type': 'string', 
	'early_career_pay': 'string', 
	'min_career_pay': 'string', 
	'percent_high_meaning': 'string'
})

row_count = 1
for row in data_table_rows:
	print(f'processing row {row_count}')

	# print(row.get_attribute('outerHTML'))
	# print(f'table row ID: {row.get_dom_attribute('id')}')

	cells = row.find_elements(By.CSS_SELECTOR, 'td.hidden-xs')

	salary_data.loc[len(salary_data)] = [
		cells[0].text,	# rank (some rows have the ra)
		cells[1].text,  # major
		cells[2].text,  # degree type
		cells[3].text,  # early career pay (in currency format - $#,###)
		cells[4].text,  # mid career pay (in currency format - $#,###)
		cells[5].text   # % high meaning (in percent format - ##%, some rows have 'N/A')
	]

	row_count += 1

script_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = os.path.join(script_dir,'salary_data.csv')

salary_data.to_csv(file_dir, index=False)

print(salary_data)