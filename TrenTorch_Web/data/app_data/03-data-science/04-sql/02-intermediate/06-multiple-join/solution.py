SELECT u.name AS user_name, p.name AS product_name, o.quantity FROM orders o JOIN users u ON u.id = o.user_id JOIN products p ON p.id = o.product_id;
