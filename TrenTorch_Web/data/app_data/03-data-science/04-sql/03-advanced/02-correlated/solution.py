SELECT * FROM users u WHERE salary > (SELECT AVG(salary) FROM users WHERE department = u.department);
