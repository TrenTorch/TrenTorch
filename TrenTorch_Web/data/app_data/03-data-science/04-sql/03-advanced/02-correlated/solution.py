SELECT name, department, salary FROM employees e WHERE salary > (SELECT AVG(salary) FROM employees WHERE department = e.department);
