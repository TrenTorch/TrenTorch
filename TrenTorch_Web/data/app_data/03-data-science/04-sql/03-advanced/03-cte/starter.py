-- SQL Schema
CREATE TABLE employees (id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1, 100000), (2, 90000), (3, 80000);

-- TODO: Use CTE to find high earners
WITH high_earners AS (SELECT * FROM employees WHERE salary > 85000) SELECT * FROM high_earners;
