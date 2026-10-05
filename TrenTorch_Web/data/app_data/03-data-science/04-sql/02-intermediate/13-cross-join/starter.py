-- @schema
CREATE TABLE colors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE sizes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
INSERT INTO colors VALUES (1, 'Red');
INSERT INTO colors VALUES (2, 'Blue');
INSERT INTO sizes VALUES (1, 'Small');
INSERT INTO sizes VALUES (2, 'Medium');
INSERT INTO sizes VALUES (3, 'Large');
-- @query
-- TODO: Return every color/size combination as color and size.

