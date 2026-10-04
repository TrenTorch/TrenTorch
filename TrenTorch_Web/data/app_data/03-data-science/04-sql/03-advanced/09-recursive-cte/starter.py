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
INSERT INTO employees VALUES (5, 'Eve', 4);
INSERT INTO employees VALUES (6, 'Frank', 3);
INSERT INTO employees VALUES (7, 'Gina', NULL);
-- @query
-- TODO: Return id, name and depth of everyone who reports to Alice (id 1), directly (depth 1) or indirectly (depth 2, 3, ...).

