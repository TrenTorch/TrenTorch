-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER
);
INSERT INTO users VALUES (1, 'Alice', 'alice@example.com', 25);
INSERT INTO users VALUES (2, 'Bob', 'bob@example.com', 30);
INSERT INTO users VALUES (3, 'Charlie', 'charlie@example.com', 35);
INSERT INTO users VALUES (4, 'Diana', 'diana@example.com', 17);
-- @query
-- TODO: Return only the name and email columns, in that order.

