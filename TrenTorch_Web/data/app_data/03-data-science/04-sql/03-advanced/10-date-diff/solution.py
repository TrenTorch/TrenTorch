SELECT name, CAST((julianday('now') - julianday(hire_date)) AS INTEGER) as days_employed FROM employees;
