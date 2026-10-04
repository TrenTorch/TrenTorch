-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
);
INSERT INTO users VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO users VALUES (2, 'Bob', NULL);
INSERT INTO users VALUES (3, 'Cara', '');
INSERT INTO users VALUES (4, 'Dan', NULL);
INSERT INTO users VALUES (5, 'Eve', 'eve@example.com');
-- @query
-- TODO: Return all columns for users whose email is NULL.

