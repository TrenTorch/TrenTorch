-- SQL Schema
CREATE TABLE users (id INTEGER, age INTEGER);
INSERT INTO users VALUES (1, 20), (2, 30), (3, 40);

-- TODO: Calculate average age
SELECT AVG(age) FROM users;
