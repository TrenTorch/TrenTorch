-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
);
INSERT INTO users VALUES (1, 'Alice', 30);
INSERT INTO users VALUES (2, 'Bob', 40);
INSERT INTO users VALUES (3, 'Charlie', 40);
INSERT INTO users VALUES (4, 'Diana', 25);
INSERT INTO users VALUES (5, 'Eve', NULL);
-- @query
-- TODO: Return the second-highest distinct age. If two users share the highest age, it is still counted once.

