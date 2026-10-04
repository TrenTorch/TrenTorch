-- SQL Schema
CREATE TABLE colors (id INTEGER, name TEXT);
CREATE TABLE sizes (id INTEGER, name TEXT);
INSERT INTO colors VALUES (1, 'Red'), (2, 'Blue');
INSERT INTO sizes VALUES (1, 'Small'), (2, 'Large');

-- TODO: Cross join
SELECT c.name, s.name FROM colors c CROSS JOIN sizes s;
