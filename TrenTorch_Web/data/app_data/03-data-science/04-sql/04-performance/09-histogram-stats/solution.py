SELECT status, COUNT(*) AS row_count, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 1) AS pct FROM orders GROUP BY status ORDER BY row_count DESC, status;
