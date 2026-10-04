-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT);
CREATE TABLE employees (id INTEGER, user_id INTEGER);
INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob');
INSERT INTO employees VALUES (1, 1), (2, 2);

-- TODO: Multiple join
SELECT u.name, e.id FROM users u JOIN employees e ON u.id = e.user_id;
