SELECT name, age, ROW_NUMBER() OVER (ORDER BY age, id) AS row_num FROM users;
