import os

import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = os.path.join(script_dir,'salary_data.csv')

salary_data = pd.read_csv(file_dir, 
                          header=0,
                          names=['rank', 'major', 'degree_type', 'early_career_pay', 'mid_career_pay', 'percent_high_meaning'])

pd.options.display.float_format = '{:,.2f}'.format

print(salary_data.head())

print('----------------')
# remove dollar sign and commas from early_career_pay and mid_career_pay columns
salary_data["early_career_pay"] = salary_data["early_career_pay"].str.replace(r'[$,]', '', regex=True)
salary_data["mid_career_pay"] = salary_data["mid_career_pay"].str.replace(r'[$,]', '', regex=True)

salary_data[["early_career_pay", "mid_career_pay"]] = salary_data[["early_career_pay", "mid_career_pay"]].astype(float)
# salary_data["early_career_pay"] = salary_data["early_career_pay"].astype(float)
# salary_data["mid_career_pay"] = salary_data["mid_career_pay"].astype(float)

print(salary_data.head())
print(salary_data['early_career_pay'].max())
print(salary_data['early_career_pay'].mean())
print(salary_data['early_career_pay'].min())