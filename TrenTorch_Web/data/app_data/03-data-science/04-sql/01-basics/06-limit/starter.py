-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT);
INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'David'), (5, 'Eve');

-- TODO: Select first 3 users
SELECT * FROM users LIMIT 3;
