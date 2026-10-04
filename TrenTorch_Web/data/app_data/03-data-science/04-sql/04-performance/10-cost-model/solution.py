WITH s AS (
  SELECT status,
         COUNT(*) AS row_count,
         ROUND(1.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 3) AS selectivity
  FROM orders
  GROUP BY status
)
SELECT status, row_count, selectivity,
       CASE WHEN selectivity < 0.15 THEN 1 ELSE 0 END AS use_index
FROM s
ORDER BY status;
