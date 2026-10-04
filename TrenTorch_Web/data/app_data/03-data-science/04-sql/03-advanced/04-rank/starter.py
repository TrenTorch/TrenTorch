-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    region TEXT NOT NULL,
    age INTEGER NOT NULL
);
INSERT INTO users VALUES (1, 'Alice', 'North', 40);
INSERT INTO users VALUES (2, 'Bob', 'North', 35);
INSERT INTO users VALUES (3, 'Charlie', 'North', 35);
INSERT INTO users VALUES (4, 'Diana', 'North', 28);
INSERT INTO users VALUES (5, 'Eve', 'South', 50);
INSERT INTO users VALUES (6, 'Frank', 'South', 31);
-- @query
-- TODO: Return name, region, age and age_rank, ranking users by age (oldest = 1) within each region. Equal ages share a rank and the next rank is skipped.

