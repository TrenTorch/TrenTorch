-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER
);
INSERT INTO users VALUES (1, 'Alice', 'alice@example.com', 25);
INSERT INTO users VALUES (2, 'Bob', 'bob@example.com', 17);
INSERT INTO users VALUES (3, 'Charlie', 'charlie@example.com', 18);
INSERT INTO users VALUES (4, 'Diana', 'diana@example.com', 16);
INSERT INTO users VALUES (5, 'Eve', 'eve@example.com', 42);
-- @query
-- TODO: Return all columns for users aged 18 or older.

