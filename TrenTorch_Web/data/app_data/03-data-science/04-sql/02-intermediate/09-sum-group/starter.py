-- @schema
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    region TEXT NOT NULL,
    amount INTEGER NOT NULL
);
INSERT INTO sales VALUES (1, 'North', 100);
INSERT INTO sales VALUES (2, 'South', 250);
INSERT INTO sales VALUES (3, 'North', 150);
INSERT INTO sales VALUES (4, 'East', 80);
INSERT INTO sales VALUES (5, 'South', 50);
INSERT INTO sales VALUES (6, 'North', 25);
-- @query
-- TODO: Return each region with its total sales amount, named total_revenue.

