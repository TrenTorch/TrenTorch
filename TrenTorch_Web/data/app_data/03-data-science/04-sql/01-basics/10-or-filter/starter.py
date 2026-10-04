-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT, department TEXT);
INSERT INTO users VALUES (1, 'Alice', 'Engineering');
INSERT INTO users VALUES (2, 'Bob', 'Sales');
INSERT INTO users VALUES (3, 'Charlie', 'HR');

-- TODO: Filter by department = 'Sales' OR 'Engineering'
SELECT * FROM users WHERE department = 'Sales' OR department = 'Engineering';
