-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT);
CREATE TABLE employees (id INTEGER, name TEXT);
INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob');
INSERT INTO employees VALUES (1, 'Charlie'), (2, 'David');

-- TODO: Union both tables
SELECT name FROM users UNION SELECT name FROM employees;
