-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
INSERT INTO users VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO users VALUES (2, 'Bob', 'bob@sample.com');
INSERT INTO users VALUES (3, 'Carol', 'carol@example.com.au');
INSERT INTO users VALUES (4, 'Dave', 'dave@EXAMPLE.COM');
INSERT INTO users VALUES (5, 'Erin', 'erin@notexample.com');
INSERT INTO users VALUES (6, 'Frank', 'frank@example.com');
-- @query
-- TODO: Return all columns for users whose email address ends with @example.com.

