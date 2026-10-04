SELECT name, salary, RANK() OVER (ORDER BY salary DESC) FROM employees;
