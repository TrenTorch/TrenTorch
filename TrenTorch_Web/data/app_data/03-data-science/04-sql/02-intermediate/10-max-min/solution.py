SELECT category, MAX(price) AS max_price, MIN(price) AS min_price FROM products GROUP BY category;
