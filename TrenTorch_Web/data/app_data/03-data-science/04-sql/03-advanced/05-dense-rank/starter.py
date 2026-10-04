-- SQL Schema
CREATE TABLE employees (id INTEGER, name TEXT, department TEXT, salary INTEGER);
INSERT INTO employees VALUES (1, 'Alice', 'Eng', 100000), (2, 'Bob', 'Eng', 90000), (3, 'Charlie', 'Sales', 80000);

-- TODO: Dense rank by department and salary
SELECT name, salary, DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) FROM employees;
