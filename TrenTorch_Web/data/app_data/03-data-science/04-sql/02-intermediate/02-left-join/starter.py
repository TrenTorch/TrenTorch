-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product TEXT NOT NULL
);
INSERT INTO users VALUES (1, 'Alice');
INSERT INTO users VALUES (2, 'Bob');
INSERT INTO users VALUES (3, 'Cara');
INSERT INTO orders VALUES (1, 1, 'Laptop');
INSERT INTO orders VALUES (2, 1, 'Mouse');
INSERT INTO orders VALUES (3, 2, 'Desk');
INSERT INTO orders VALUES (4, 99, 'Ghost item');
-- @query
-- TODO: Return id, name and order_count for every user, including users with no orders.

