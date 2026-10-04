-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER
);
INSERT INTO users VALUES (1, 'Alice', 'alice@example.com', 25);
INSERT INTO users VALUES (2, 'Adam', 'adam@example.com', 17);
INSERT INTO users VALUES (3, 'Bob', 'bob@example.com', 30);
INSERT INTO users VALUES (4, 'Anna', 'anna@example.com', 40);
INSERT INTO users VALUES (5, 'Aaron', 'aaron@example.com', 18);
INSERT INTO users VALUES (6, 'Zara', 'zara@example.com', 22);
-- @query
-- TODO: Return all columns for users aged 18 or over whose name starts with the letter A.

