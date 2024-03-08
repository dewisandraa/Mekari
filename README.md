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
