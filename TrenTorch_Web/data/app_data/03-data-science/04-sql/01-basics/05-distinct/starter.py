-- SQL Schema
CREATE TABLE users (id INTEGER, age INTEGER);
INSERT INTO users VALUES (1, 25), (2, 25), (3, 30), (4, 30), (5, 35);

-- TODO: Select distinct ages
SELECT DISTINCT age FROM users;
