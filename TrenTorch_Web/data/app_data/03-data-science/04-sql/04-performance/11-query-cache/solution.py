WITH totals AS MATERIALIZED (
  SELECT customer_id, SUM(total) AS spend
  FROM orders
  GROUP BY customer_id
)
SELECT customer_id, spend
FROM totals
WHERE spend > (SELECT AVG(spend) FROM totals)
ORDER BY spend DESC, customer_id
LIMIT 5;
