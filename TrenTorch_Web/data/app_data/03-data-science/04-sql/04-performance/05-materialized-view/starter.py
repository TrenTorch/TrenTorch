-- @schema
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    region TEXT NOT NULL,
    product TEXT NOT NULL,
    amount INTEGER NOT NULL
);
WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 2000)
INSERT INTO sales
SELECT i,
       CASE i % 4 WHEN 0 THEN 'North' WHEN 1 THEN 'South' WHEN 2 THEN 'East' ELSE 'West' END,
       'product_' || (i % 20),
       (i * 13) % 200 + 5
FROM n;
-- @query
-- TODO: Create a table named sales_by_region holding each region's total_amount and order_count
-- (CREATE TABLE ... AS SELECT), then SELECT everything from it ordered by region.

