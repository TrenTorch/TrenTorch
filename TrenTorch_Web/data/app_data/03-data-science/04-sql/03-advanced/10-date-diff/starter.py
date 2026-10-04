-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    registered_on TEXT NOT NULL
);
INSERT INTO users VALUES (1, 'Alice', '1990-03-15', '2024-01-01');
INSERT INTO users VALUES (2, 'Bob', '2000-12-31', '2024-06-01');
INSERT INTO users VALUES (3, 'Charlie', '1985-06-30', '2023-06-30');
-- @query
-- TODO: As of 2024-06-30, return name, age_years (completed years since birth_date) and days_registered (whole days since registered_on).

