-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
);
INSERT INTO users VALUES (1, 'Alice', 25);
INSERT INTO users VALUES (2, 'Bob', 30);
INSERT INTO users VALUES (3, 'Charlie', 35);
INSERT INTO users VALUES (4, 'Diana', 40);
INSERT INTO users VALUES (5, 'Eve', 20);
-- @query
-- TODO: Return id, name and age of every user older than the average age of all users.

