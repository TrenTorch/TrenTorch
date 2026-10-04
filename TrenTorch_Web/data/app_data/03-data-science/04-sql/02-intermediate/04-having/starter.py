-- SQL Schema
CREATE TABLE users (id INTEGER, department TEXT);
INSERT INTO users VALUES (1, 'Engineering'), (2, 'Engineering'), (3, 'Sales'), (4, 'Sales'), (5, 'Sales');

-- TODO: Find departments with more than 2 users
SELECT department, COUNT(*) as cnt FROM users GROUP BY department HAVING COUNT(*) > 2;
