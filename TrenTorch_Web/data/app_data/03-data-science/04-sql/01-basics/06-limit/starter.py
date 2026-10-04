-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
);
INSERT INTO users VALUES (1, 'Alice', 25);
INSERT INTO users VALUES (2, 'Bob', 30);
INSERT INTO users VALUES (3, 'Charlie', 35);
INSERT INTO users VALUES (4, 'Diana', 28);
INSERT INTO users VALUES (5, 'Eve', 41);
INSERT INTO users VALUES (6, 'Frank', 19);
INSERT INTO users VALUES (7, 'Gina', 52);
-- @query
-- TODO: Return page 2 of the users (2 rows per page), ordered by id.

