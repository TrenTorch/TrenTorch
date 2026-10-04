SELECT e.name AS employee, m.name AS manager FROM employees e JOIN employees m ON m.id = e.manager_id;
