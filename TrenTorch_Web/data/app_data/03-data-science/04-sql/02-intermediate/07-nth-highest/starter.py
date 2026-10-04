-- SQL Schema
CREATE TABLE employees (id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1, 100000), (2, 90000), (3, 80000), (4, 70000), (5, 60000);

-- TODO: Find 3rd highest salary
SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 2;
