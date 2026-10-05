-- @schema
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary INTEGER NOT NULL
);
INSERT INTO employees VALUES (1, 'Alice', 'Engineering', 50000);
INSERT INTO employees VALUES (2, 'Bob', 'Engineering', 60000);
INSERT INTO employees VALUES (3, 'Charlie', 'Engineering', 90000);
INSERT INTO employees VALUES (4, 'Diana', 'Sales', 40000);
INSERT INTO employees VALUES (5, 'Eve', 'Sales', 44000);
INSERT INTO employees VALUES (6, 'Frank', 'HR', 52000);
-- @query
-- TODO: Using a WITH clause, compute each department's average salary first, then return name, department and salary of employees earning more than their department's average.

