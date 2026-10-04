SELECT user_id, COUNT(*) AS order_count FROM orders GROUP BY user_id HAVING COUNT(*) > 1;
