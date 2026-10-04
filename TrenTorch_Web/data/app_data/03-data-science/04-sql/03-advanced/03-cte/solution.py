WITH dept_avg AS (
  SELECT department, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY department
)
SELECT e.name, e.department, e.salary
FROM employees e
JOIN dept_avg d ON d.department = e.department
WHERE e.salary > d.avg_salary;
