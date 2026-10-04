SELECT department, COUNT(*) as cnt FROM users GROUP BY department HAVING COUNT(*) > 2;
