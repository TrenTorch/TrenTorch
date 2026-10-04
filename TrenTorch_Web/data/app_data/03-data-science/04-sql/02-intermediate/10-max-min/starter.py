-- SQL Schema
CREATE TABLE employees (id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1, 50000), (2, 90000), (3, 30000);

-- TODO: Find max and min salary
SELECT MAX(salary), MIN(salary) FROM employees;
