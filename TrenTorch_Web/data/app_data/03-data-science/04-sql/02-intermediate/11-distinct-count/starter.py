-- @schema
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product TEXT NOT NULL
);
INSERT INTO orders VALUES (1, 1, 'Laptop');
INSERT INTO orders VALUES (2, 1, 'Mouse');
INSERT INTO orders VALUES (3, 2, 'Desk');
INSERT INTO orders VALUES (4, 3, 'Chair');
INSERT INTO orders VALUES (5, 3, 'Lamp');
INSERT INTO orders VALUES (6, 3, 'Monitor');
-- @query
-- TODO: Return how many different customers placed at least one order, as customer_count.

