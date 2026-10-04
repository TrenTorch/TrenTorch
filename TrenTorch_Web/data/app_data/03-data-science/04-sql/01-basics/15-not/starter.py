-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT, department TEXT);
INSERT INTO users VALUES (1, 'Alice', 'Engineering');
INSERT INTO users VALUES (2, 'Bob', 'Sales');
INSERT INTO users VALUES (3, 'Charlie', 'Engineering');

-- TODO: Find non-Sales department employees
SELECT * FROM users WHERE NOT department = 'Sales';
