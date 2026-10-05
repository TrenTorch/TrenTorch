-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
CREATE TABLE archive_users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
INSERT INTO users VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO users VALUES (2, 'Bob', 'bob@example.com');
INSERT INTO users VALUES (3, 'Cara', 'cara@example.com');
INSERT INTO archive_users VALUES (3, 'Cara', 'cara@example.com');
INSERT INTO archive_users VALUES (7, 'Gus', 'gus@example.com');
-- @query
-- TODO: Return id, name and email of every person who appears in users or archive_users, listing each person once.

