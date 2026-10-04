-- SQL Schema
CREATE TABLE users (id INTEGER, name TEXT, age INTEGER);
INSERT INTO users VALUES (1, 'Alice', 25), (2, 'Bob', 35), (3, 'Charlie', 45);

-- TODO: Categorize by age
SELECT name, CASE WHEN age < 30 THEN 'Young' ELSE 'Senior' END FROM users;
