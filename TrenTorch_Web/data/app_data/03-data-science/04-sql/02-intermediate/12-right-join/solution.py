SELECT o.id AS order_id, u.name FROM users u RIGHT JOIN orders o ON o.user_id = u.id;
