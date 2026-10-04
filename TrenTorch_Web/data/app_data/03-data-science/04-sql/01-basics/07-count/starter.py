-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT);
INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie');

-- TODO: Count all users
SELECT COUNT(*) FROM users;
