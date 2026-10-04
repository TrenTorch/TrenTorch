-- SQL Schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
);

INSERT INTO users VALUES (1, 'Charlie', 35);
INSERT INTO users VALUES (2, 'Alice', 25);
INSERT INTO users VALUES (3, 'Bob', 30);

-- TODO: Select all users sorted by age in descending order
SELECT * FROM users ORDER BY age DESC;
