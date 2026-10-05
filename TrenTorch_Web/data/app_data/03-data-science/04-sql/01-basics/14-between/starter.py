-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
);
INSERT INTO users VALUES (1, 'Alice', 29);
INSERT INTO users VALUES (2, 'Bob', 30);
INSERT INTO users VALUES (3, 'Charlie', 35);
INSERT INTO users VALUES (4, 'Diana', 40);
INSERT INTO users VALUES (5, 'Eve', 41);
INSERT INTO users VALUES (6, 'Frank', 22);
-- @query
-- TODO: Return all columns for users aged 30 to 40, both ends included.

