CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    branch_id INT,
    salary DECIMAL(10, 2),
    join_date DATE,
    resign_date DATE
);

LOAD DATA 
    INFILE './datasets/employees.csv'
    INTO TABLE employees
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;

CREATE TABLE timesheets (
    timesheet_id INT PRIMARY KEY,
    employee_id INT,
    date DATE,
    checkin TIME,
    checkout TIME,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

LOAD DATA INFILE './datasets/timesheets.csv'
INTO TABLE timesheets
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

DROP TABLE IF EXISTS salary_per_hour;

CREATE TABLE salary_per_hour_by_branch AS
WITH employee_hours AS (
    SELECT 
        e.branch_id, 
        EXTRACT(YEAR FROM t.date) AS year, 
        EXTRACT(MONTH FROM t.date) AS month, 
        t.employee_id, 
        SUM(EXTRACT(EPOCH FROM (checkout - checkin))/3600) AS total_hours -- Convert seconds to hours
    FROM timesheets t
    JOIN employees e ON t.employee_id = e.employee_id
    WHERE t.checkout IS NOT NULL -- Ensuring checkout is recorded
    GROUP BY e.branch_id, year, month, t.employee_id
), aggregated_data AS (
    SELECT 
        branch_id, 
        year, 
        month, 
        SUM(salary) AS total_salary, 
        SUM(total_hours) AS total_hours
    FROM employee_hours eh
    JOIN employees e ON eh.employee_id = e.employee_id
    GROUP BY branch_id, year, month
)
SELECT 
    year, 
    month, 
    branch_id, 
    (total_salary / total_hours) AS salary_per_hour
FROM aggregated_data;

CREATE INDEX idx_salary_per_hour ON salary_per_hour(year, month, branch_id);