-- SQL Schema
CREATE TABLE employees (id INTEGER, department TEXT, salary INTEGER);
INSERT INTO employees VALUES (1, 'Engineering', 50000), (2, 'Engineering', 60000), (3, 'Sales', 40000);

-- TODO: Sum salaries by department
SELECT department, SUM(salary) FROM employees GROUP BY department;
