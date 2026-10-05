SELECT o.user_id, o.product, u.name FROM orders o JOIN users u ON u.id = o.user_id;
