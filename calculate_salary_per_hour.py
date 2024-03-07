import pandas as pd
from datetime import datetime, timedelta

def load_data(employees_file, timesheets_file):
    """
    Loads employees and timesheets data from CSV files and prepares them for processing.
    """
    # Load data
    employees_df = pd.read_csv(employees_file)
    timesheets_df = pd.read_csv(timesheets_file)

    # Ensure consistent column naming
    employees_df.rename(columns={"employe_id": "employee_id"}, inplace=True)

    timesheets_df["date"] = pd.to_datetime(timesheets_df['date'])

    employees_df['join_date'] = pd.to_datetime(employees_df['join_date'])
    employees_df['resign_date'] = pd.to_datetime(employees_df['resign_date'].fillna(datetime.now()))

    return employees_df, timesheets_df

def time_to_seconds(t):
    return (t.hour * 3600 + t.minute * 60 + t.second) if t is not pd.NaT else None

def seconds_to_time(seconds):
    """Convert seconds past midnight to a %H:%M:%S time string."""
    if seconds is None:
        return None
    return (datetime.min + timedelta(seconds=seconds)).time().strftime('%H:%M:%S')

def impute_missing_times(timesheets_df):
    """
    Imputes missing check-in and check-out times based on the average of check-in and check-out times for each employee_id
    and recalculates working hours.
    """

    timesheets_df['checkin'] = pd.to_datetime(timesheets_df['checkin'], format='%H:%M:%S', errors='coerce').dt.time
    timesheets_df['checkout'] = pd.to_datetime(timesheets_df['checkout'], format='%H:%M:%S', errors='coerce').dt.time

    # Convert check-in and check-out times to seconds for averaging
    timesheets_df['checkin_seconds'] = timesheets_df['checkin'].apply(time_to_seconds)
    timesheets_df['checkout_seconds'] = timesheets_df['checkout'].apply(time_to_seconds)
    
    # Calculate mean check-in and check-out times in seconds for each employee
    avg_times = timesheets_df.groupby('employee_id')[['checkin_seconds', 'checkout_seconds']].mean()

    # Join the average times back to the original dataframe
    timesheets_df = pd.merge(timesheets_df, avg_times, on='employee_id', suffixes=('', '_avg'))
    
    # Impute missing check-in and check-out times
    timesheets_df.loc[pd.isnull(timesheets_df['checkin_seconds']), 'checkin_seconds'] = timesheets_df['checkin_seconds_avg']
    timesheets_df.loc[pd.isnull(timesheets_df['checkout_seconds']), 'checkout_seconds'] = timesheets_df['checkout_seconds_avg']
    
    # Convert seconds back to %H:%M:%S format for imputed check-in and check-out times
    timesheets_df['imputed_checkin'] = timesheets_df['checkin_seconds'].apply(seconds_to_time)
    timesheets_df['imputed_checkout'] = timesheets_df['checkout_seconds'].apply(seconds_to_time)
    
    # Calculate working hours based on seconds
    timesheets_df['working_hours'] = (timesheets_df['checkout_seconds'] - timesheets_df['checkin_seconds']) / 3600.0
    
    # Clean up the dataframe by removing temporary columns
    timesheets_df.drop(['checkin_seconds', 'checkout_seconds', 'checkin_seconds_avg', 'checkout_seconds_avg'], axis=1, inplace=True)
    timesheets_df = timesheets_df[timesheets_df["working_hours"] > 0]
    
    return timesheets_df


def calculate_salary_per_hour(employees_df, timesheets_df):
    """
    Calculates the salary per hour for each branch, per month.
    """
    # Merge datasets
    merged_df = pd.merge(timesheets_df, employees_df, on='employee_id')
    merged_df = merged_df[(merged_df['date'] >= merged_df['join_date']) & (merged_df['date'] <= merged_df['resign_date'])]

    # Extract year and month
    merged_df['year'] = merged_df['date'].dt.year
    merged_df['month'] = merged_df['date'].dt.month

    # Aggregate by year, month, and branch to calculate total salary and total hours
    aggregated_df = merged_df.groupby(['year', 'month', 'branch_id']).agg(total_salary=('salary', 'sum'), total_hours=('working_hours', 'sum')).reset_index()

    # Calculate salary per hour
    aggregated_df['salary_per_hour'] = round(aggregated_df['total_salary'] / aggregated_df['total_hours'].replace(0, pd.NA),2)

    return aggregated_df[['year', 'month', 'branch_id', 'salary_per_hour']]

def main():
    employees_df, timesheets_df = load_data('./datasets/employees.csv', './datasets/timesheets.csv')
    timesheets_df = impute_missing_times(timesheets_df)
    salary_per_hour_df = calculate_salary_per_hour(employees_df, timesheets_df)
    print(salary_per_hour_df)
    #Append or update to a db with new calculations
    # salary_per_hour_df.to_sql('salary_per_hour_table', engine, if_exists='append', index=False)

if __name__ == "__main__":
    main()
