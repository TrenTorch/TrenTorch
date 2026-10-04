-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER
);
INSERT INTO users VALUES (1, 'Charlie', 'charlie@example.com', 35);
INSERT INTO users VALUES (2, 'Alice', 'alice@example.com', 25);
INSERT INTO users VALUES (3, 'Eve', 'eve@example.com', 41);
INSERT INTO users VALUES (4, 'Bob', 'bob@example.com', 30);
-- @query
-- TODO: Return all columns, sorted by age from highest to lowest.

