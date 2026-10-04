-- SQL Schema (no table needed)
-- TODO: Generate numbers 1 to 5 using recursive CTE
WITH RECURSIVE nums(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM nums WHERE n < 5) SELECT * FROM nums;
