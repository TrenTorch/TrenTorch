SELECT name, salary, LEAD(salary) OVER (ORDER BY salary DESC) FROM employees;
