-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
);
INSERT INTO users VALUES (1, 'Alice', 20);
INSERT INTO users VALUES (2, 'Bob', 30);
INSERT INTO users VALUES (3, 'Charlie', 40);
INSERT INTO users VALUES (4, 'Diana', NULL);
INSERT INTO users VALUES (5, 'Eve', 50);
-- @query
-- TODO: Return the average age of all users.

