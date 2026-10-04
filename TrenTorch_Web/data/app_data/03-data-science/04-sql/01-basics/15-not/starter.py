-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
);
INSERT INTO users VALUES (1, 'Alice', 25);
INSERT INTO users VALUES (2, 'Bob', 30);
INSERT INTO users VALUES (3, 'Carl', 35);
INSERT INTO users VALUES (4, 'chris', 28);
INSERT INTO users VALUES (5, 'Dana', 41);
INSERT INTO users VALUES (6, 'Eli', 19);
-- @query
-- TODO: Return all columns for users whose name does NOT start with the letter C.

