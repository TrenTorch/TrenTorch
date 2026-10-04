SELECT u.name, e.salary FROM users u LEFT JOIN employees e ON u.id = e.user_id;
