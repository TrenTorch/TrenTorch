SELECT name, region, age, RANK() OVER (PARTITION BY region ORDER BY age DESC) AS age_rank FROM users;
