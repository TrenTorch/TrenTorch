-- @schema
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product TEXT NOT NULL,
    amount INTEGER NOT NULL
);
INSERT INTO orders VALUES (1, 1, 'Laptop', 900);
INSERT INTO orders VALUES (2, 1, 'Mouse', 20);
INSERT INTO orders VALUES (3, 2, 'Desk', 150);
INSERT INTO orders VALUES (4, 3, 'Chair', 80);
INSERT INTO orders VALUES (5, 3, 'Lamp', 30);
INSERT INTO orders VALUES (6, 3, 'Monitor', 200);
-- @query
-- TODO: Return each user_id with the number of orders they placed, as order_count.

