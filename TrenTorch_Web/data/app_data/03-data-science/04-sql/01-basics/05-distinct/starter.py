-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL
);
INSERT INTO users VALUES (1, 'Alice', 'Pune');
INSERT INTO users VALUES (2, 'Bob', 'Mumbai');
INSERT INTO users VALUES (3, 'Charlie', 'Pune');
INSERT INTO users VALUES (4, 'Diana', 'Delhi');
INSERT INTO users VALUES (5, 'Eve', 'Mumbai');
INSERT INTO users VALUES (6, 'Frank', 'Pune');
-- @query
-- TODO: Return each city that appears in users exactly once.

