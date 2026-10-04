-- SQL Schema
CREATE TABLE employees (id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES (1, 'Alice', 100000), (2, 'Bob', 90000), (3, 'Charlie', 90000), (4, 'David', 80000);

-- TODO: Rank employees by salary
SELECT name, salary, RANK() OVER (ORDER BY salary DESC) FROM employees;
