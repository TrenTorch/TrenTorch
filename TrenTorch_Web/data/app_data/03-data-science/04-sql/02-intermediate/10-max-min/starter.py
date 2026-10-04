-- @schema
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price INTEGER NOT NULL
);
INSERT INTO products VALUES (1, 'Laptop', 'Electronics', 900);
INSERT INTO products VALUES (2, 'Mouse', 'Electronics', 20);
INSERT INTO products VALUES (3, 'Desk', 'Furniture', 150);
INSERT INTO products VALUES (4, 'Chair', 'Furniture', 80);
INSERT INTO products VALUES (5, 'Lamp', 'Furniture', 30);
INSERT INTO products VALUES (6, 'Pen', 'Stationery', 2);
-- @query
-- TODO: For each category return its highest and lowest price as max_price and min_price.

