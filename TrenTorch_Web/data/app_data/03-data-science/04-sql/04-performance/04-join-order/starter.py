-- @schema
CREATE TABLE regions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    region_id INTEGER NOT NULL,
    name TEXT NOT NULL
);
INSERT INTO regions VALUES (1, 'EU'), (2, 'US'), (3, 'APAC'), (4, 'LATAM'), (5, 'MEA');
WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 1000)
INSERT INTO customers SELECT i, i % 5 + 1, 'customer_' || i FROM n;
CREATE INDEX idx_customers_region ON customers(region_id);
-- @query
-- TODO: List the names of customers in region 'EU'. Join regions and customers with CROSS JOIN so SQLite
-- loops over the small regions table first and looks up customers through idx_customers_region.
-- Do not alias the tables.

