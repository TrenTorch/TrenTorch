-- SQL Schema
CREATE TABLE users (id INTEGER, department TEXT);
INSERT INTO users VALUES (1, 'Engineering'), (2, 'Engineering'), (3, 'Sales'), (4, 'Sales'), (5, 'HR');

-- TODO: Count users by department
SELECT department, COUNT(*) as count FROM users GROUP BY department;
