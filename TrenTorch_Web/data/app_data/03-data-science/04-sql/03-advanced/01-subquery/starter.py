-- SQL Schema
CREATE TABLE users (id INTEGER);
CREATE TABLE orders (id INTEGER, user_id INTEGER);
INSERT INTO users VALUES (1), (2), (3);
INSERT INTO orders VALUES (1, 1), (2, 1), (3, 2);

-- TODO: Find users with orders
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);
