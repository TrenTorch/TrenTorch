-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT, department TEXT, salary INTEGER);
INSERT INTO users VALUES (1, 'Alice', 'Engineering', 50000);
INSERT INTO users VALUES (2, 'Bob', 'Engineering', 60000);
INSERT INTO users VALUES (3, 'Charlie', 'Sales', 40000);

-- TODO: Find users earning more than their department average
SELECT * FROM users u WHERE salary > (SELECT AVG(salary) FROM users WHERE department = u.department);
