-- SQL Schema (auto-loaded by executor)
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER
);

INSERT INTO users VALUES (1, 'Alice', 'alice@example.com', 25);
INSERT INTO users VALUES (2, 'Bob', 'bob@example.com', 30);
INSERT INTO users VALUES (3, 'Charlie', 'charlie@example.com', 35);

-- TODO: Write your SQL query here
-- Your query should select all rows from the users table
SELECT * FROM users;
