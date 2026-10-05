-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL
);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL
);
INSERT INTO users VALUES (1, 'Alice');
INSERT INTO users VALUES (2, 'Bob');
INSERT INTO products VALUES (1, 'Laptop', 900);
INSERT INTO products VALUES (2, 'Mouse', 20);
INSERT INTO products VALUES (3, 'Desk', 150);
INSERT INTO orders VALUES (1, 1, 1, 1);
INSERT INTO orders VALUES (2, 1, 2, 3);
INSERT INTO orders VALUES (3, 2, 3, 2);
-- @query
-- TODO: Return user_name, product_name and quantity for every order, joining users, orders and products.

