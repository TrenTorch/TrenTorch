-- SQL Schema
CREATE TABLE users (id INTEGER, first_name TEXT, last_name TEXT);
INSERT INTO users VALUES (1, 'John', 'Doe'), (2, 'Jane', 'Smith');

-- TODO: Concatenate names
SELECT CONCAT(first_name, ' ', last_name) FROM users;
