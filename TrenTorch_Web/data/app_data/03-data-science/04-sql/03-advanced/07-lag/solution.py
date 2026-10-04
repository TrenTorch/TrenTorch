SELECT name, salary, LAG(salary) OVER (ORDER BY salary DESC) FROM employees;
