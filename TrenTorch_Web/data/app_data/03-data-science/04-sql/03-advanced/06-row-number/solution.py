SELECT name, ROW_NUMBER() OVER (ORDER BY salary DESC) FROM employees;
