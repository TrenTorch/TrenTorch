-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
);
INSERT INTO users VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO users VALUES (2, 'Bob', NULL);
INSERT INTO users VALUES (3, 'Charlie', 'charlie@example.com');
INSERT INTO users VALUES (4, 'Diana', NULL);
INSERT INTO users VALUES (5, 'Eve', 'eve@example.com');
-- @query
-- TODO: Return the total number of users, including users with no email.

