SELECT id, name, age FROM users WHERE age > (SELECT AVG(age) FROM users);
