-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
);
INSERT INTO users VALUES (1, 'Alice', 30);
INSERT INTO users VALUES (2, 'Bob', 25);
INSERT INTO users VALUES (3, 'Charlie', 30);
INSERT INTO users VALUES (4, 'Diana', 22);
INSERT INTO users VALUES (5, 'Eve', 41);
-- @query
-- TODO: Return name, age and row_num: a unique sequence 1, 2, 3, ... ordered by age ascending, breaking ties by id.

