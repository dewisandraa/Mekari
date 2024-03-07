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

CREATE TABLE salary_per_hour AS 
    SELECT 
        YEAR(t.date) AS year, 
        MONTH(t.date) AS month, 
        e.branch_id, 
        SUM(e.salary) / NULLIF(SUM(TIMESTAMPDIFF(HOUR, t.checkin, COALESCE(t.checkout, t.checkin))), 0) AS salary_per_hour
    FROM 
        timesheets t
    JOIN 
        employees e ON t.employee_id = e.employee_id
    WHERE 
        t.checkout IS NOT NULL
        AND t.checkin <= t.checkout
        AND (e.resign_date IS NULL OR e.resign_date >= t.date)
    GROUP BY 
        YEAR(t.date), 
        MONTH(t.date), 
        e.branch_id
;

CREATE INDEX idx_salary_per_hour ON salary_per_hour(year, month, branch_id);