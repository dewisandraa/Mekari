CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    branch_id INT,
    salary DECIMAL(10, 2),
    join_date DATE,
    resign_date DATE
);

CREATE TABLE timesheets (
    timesheet_id INT PRIMARY KEY,
    employee_id INT,
    date DATE,
    checkin TIME,
    checkout TIME,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

