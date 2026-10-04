-- SQL Schema
CREATE TABLE employees (id INTEGER, name TEXT, manager_id INTEGER);
INSERT INTO employees VALUES (1, 'Alice', NULL);
INSERT INTO employees VALUES (2, 'Bob', 1);
INSERT INTO employees VALUES (3, 'Charlie', 1);

-- TODO: Find employees with no manager
SELECT * FROM employees WHERE manager_id IS NULL;
