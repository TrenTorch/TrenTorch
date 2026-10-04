-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT);
INSERT INTO users VALUES (1, 'Alice');
INSERT INTO users VALUES (2, 'Bob');
INSERT INTO users VALUES (3, 'Charlie');

-- TODO: Find names containing 'li'
SELECT * FROM users WHERE name LIKE '%li%';
