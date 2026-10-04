-- SQL Schema
CREATE TABLE users (id INTEGER, department TEXT);
INSERT INTO users VALUES (1, 'Engineering'), (2, 'Engineering'), (3, 'Sales'), (4, 'Sales'), (5, 'HR');

-- TODO: Count distinct departments
SELECT COUNT(DISTINCT department) FROM users;
