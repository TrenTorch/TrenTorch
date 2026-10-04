SELECT name, salary, DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) FROM employees;
