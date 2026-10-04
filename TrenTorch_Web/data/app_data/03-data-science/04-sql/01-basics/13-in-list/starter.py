-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
);
INSERT INTO users VALUES (1, 'Alice', 12);
INSERT INTO users VALUES (2, 'Bob', 13);
INSERT INTO users VALUES (3, 'Charlie', 16);
INSERT INTO users VALUES (4, 'Diana', 17);
INSERT INTO users VALUES (5, 'Eve', 66);
INSERT INTO users VALUES (6, 'Frank', 40);
INSERT INTO users VALUES (7, 'Gina', 12);
-- @query
-- TODO: Return all columns for users whose age is exactly 12, 16 or 66.

