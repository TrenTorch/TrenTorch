-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT);
CREATE TABLE employees (id INTEGER, user_id INTEGER, salary INTEGER);
INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie');
INSERT INTO employees VALUES (1, 1, 50000), (2, 2, 60000);

-- TODO: Left join users and employees
SELECT u.name, e.salary FROM users u LEFT JOIN employees e ON u.id = e.user_id;
