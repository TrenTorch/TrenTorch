-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT
);
INSERT INTO users VALUES (1, 'John', 'Doe');
INSERT INTO users VALUES (2, 'Jane', 'Smith');
INSERT INTO users VALUES (3, 'Prince', NULL);
-- @query
-- TODO: Return each user's full name as full_name (first name, a space, last name). If there is no last name, return just the first name.

