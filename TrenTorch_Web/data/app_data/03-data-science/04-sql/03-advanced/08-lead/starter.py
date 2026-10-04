-- SQL Schema
CREATE TABLE employees (id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES (1, 'Alice', 100000), (2, 'Bob', 90000), (3, 'Charlie', 80000);

-- TODO: Get next salary
SELECT name, salary, LEAD(salary) OVER (ORDER BY salary DESC) FROM employees;
