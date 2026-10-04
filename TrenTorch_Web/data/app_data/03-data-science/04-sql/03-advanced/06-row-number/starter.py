-- SQL Schema
CREATE TABLE employees (id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES (1, 'Alice', 100000), (2, 'Bob', 90000), (3, 'Charlie', 80000);

-- TODO: Assign row numbers
SELECT name, ROW_NUMBER() OVER (ORDER BY salary DESC) FROM employees;
