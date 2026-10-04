-- @schema
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    manager_id INTEGER
);
INSERT INTO employees VALUES (1, 'Alice', NULL);
INSERT INTO employees VALUES (2, 'Bob', 1);
INSERT INTO employees VALUES (3, 'Charlie', 1);
INSERT INTO employees VALUES (4, 'Diana', 2);
-- @query
-- TODO: Return each employee's name as employee and their manager's name as manager. Skip employees who have no manager.

