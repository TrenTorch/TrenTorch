-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT, age INTEGER);
INSERT INTO users VALUES (1, 'Alice', 20);
INSERT INTO users VALUES (2, 'Bob', 25);
INSERT INTO users VALUES (3, 'Charlie', 30);
INSERT INTO users VALUES (4, 'David', 35);

-- TODO: Find ages between 25 and 30
SELECT * FROM users WHERE age BETWEEN 25 AND 30;
