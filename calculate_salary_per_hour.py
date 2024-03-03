import pandas as pd

employees_df = pd.read_csv('./datasets/employees.csv')
timesheets_df = pd.read_csv('./datasets/timesheets.csv')

print(employees_df)
print(timesheets_df)