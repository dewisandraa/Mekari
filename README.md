# Mekari

## Overview

The analysis pipeline consists of two main components:
- An SQL script for creating schemas, loading data into a database, and transforming this data to obtain salary per hour calculations.
- A Python script for loading, cleaning, imputing missing timesheet entries, and calculating salary per hour before loading the results into a database.

## SQL Script

The SQL portion of this project involves:
1. Creating `employees` and `timesheets` tables based on the provided CSV files.
2. A transformation script that calculates the total working hours per employee per month, aggregates this data by branch and month, and computes the salary per hour for each branch.

### Schema Creation

Tables are defined with specific data types for accurate data representation, including handling potential null values in fields such as `resign_date` and `checkout`.

### Data Transformation

The transformation script computes salary per hour by:
- Calculating total hours worked by each employee per month.
- Aggregating total salaries and hours worked by branch and month.
- Calculating the salary per hour for each branch on a monthly basis.

The resulting data is loaded into a destination table

# Python Script

The Python script performs the following tasks:

### `load_data`
- **Purpose**: Loads employees and timesheets data from CSV files, ensuring data consistency and preparing it for processing.
- **Inputs**:
  - `employees_file`: The path to the employees CSV file.
  - `timesheets_file`: The path to the timesheets CSV file.
- **Process**:
  1. Loads data into DataFrames.
  2. Renames columns to ensure consistency.
  3. Converts date columns to datetime format.
- **Outputs**: Returns prepared DataFrames for employees and timesheets.

### `time_to_seconds` and `seconds_to_time`
- **Purpose**: Helper functions to convert times to seconds and seconds to time strings, facilitating time calculations.

### `impute_missing_times`
- **Purpose**: Imputes missing check-in and check-out times based on the average times for each employee and recalculates working hours.
- **Inputs**:
  - `timesheets_df`: DataFrame containing timesheets data.
- **Process**:
  1. Converts check-in and check-out times to seconds.
  2. Calculates mean check-in and check-out times in seconds for each employee.
  3. Imputes missing times with average times.
  4. Converts seconds back to time format.
  5. Calculates working hours.
  6. Cleans up temporary columns.
- **Outputs**: Updated timesheets DataFrame with imputed times and calculated working hours.

### `calculate_salary_per_hour`
- **Purpose**: Calculates the salary per hour for each branch, per month.
- **Inputs**:
  - `employees_df`: DataFrame containing employees data.
  - `timesheets_df`: DataFrame containing timesheets data with imputed times.
- **Process**:
  1. Merges employees and timesheets DataFrames.
  2. Filters data for valid employment periods.
  3. Extracts year and month from dates.
  4. Aggregates data by year, month, and branch to calculate total salary and total hours.
  5. Calculates salary per hour.
- **Outputs**: DataFrame containing the salary per hour for each branch, per month.

## Main Script

The `main` function orchestrates the execution of the script, including data loading, processing, and calculation of salary per hour. The output table is then appended to a database. 
