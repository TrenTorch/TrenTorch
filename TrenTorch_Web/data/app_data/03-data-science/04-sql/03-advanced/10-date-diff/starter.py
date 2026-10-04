-- SQL Schema
CREATE TABLE employees (id INTEGER, name TEXT, hire_date TEXT);
INSERT INTO employees VALUES (1, 'Alice', '2020-01-01'), (2, 'Bob', '2021-06-15');

-- TODO: Calculate days employed
SELECT name, CAST((julianday('now') - julianday(hire_date)) AS INTEGER) as days_employed FROM employees;
