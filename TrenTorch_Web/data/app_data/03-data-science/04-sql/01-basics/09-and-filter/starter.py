-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT, age INTEGER, department TEXT);
INSERT INTO users VALUES (1, 'Alice', 25, 'Engineering');
INSERT INTO users VALUES (2, 'Bob', 30, 'Engineering');
INSERT INTO users VALUES (3, 'Charlie', 35, 'Sales');

-- TODO: Filter by age > 25 AND department = 'Engineering'
SELECT * FROM users WHERE age > 25 AND department = 'Engineering';
