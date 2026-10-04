-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT);
CREATE TABLE employees (id INTEGER, user_id INTEGER);
INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob');
INSERT INTO employees VALUES (1, 1);

-- TODO: Right join (or simulate with left join reversed)
SELECT u.name FROM employees e RIGHT JOIN users u ON e.user_id = u.id;
