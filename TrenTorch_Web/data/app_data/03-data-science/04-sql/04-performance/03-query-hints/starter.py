-- @schema
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    total INTEGER NOT NULL,
    created_on TEXT NOT NULL
);
WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 5000)
INSERT INTO orders
SELECT i,
       i % 500 + 1,
       CASE i % 10 WHEN 0 THEN 'returned' WHEN 1 THEN 'new' WHEN 2 THEN 'shipped' WHEN 3 THEN 'shipped' ELSE 'paid' END,
       (i * 37) % 400 + 10,
       date('2024-01-01', '+' || (i % 366) || ' days')
FROM n;

CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_on);
-- @query
-- TODO: Count the paid orders created on or after 2024-06-01 and FORCE SQLite to use idx_orders_created
-- with INDEXED BY.

