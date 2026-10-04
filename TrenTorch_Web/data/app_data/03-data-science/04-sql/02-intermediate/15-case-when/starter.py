-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
);
INSERT INTO users VALUES (1, 'Alice', 12);
INSERT INTO users VALUES (2, 'Bob', 17);
INSERT INTO users VALUES (3, 'Charlie', 18);
INSERT INTO users VALUES (4, 'Diana', 64);
INSERT INTO users VALUES (5, 'Eve', 65);
INSERT INTO users VALUES (6, 'Frank', 40);
-- @query
-- TODO: Return each user's name and an age_group: 'minor' (under 18), 'adult' (18 to 64) or 'senior' (65 and over).

