CREATE TABLE sales_by_region AS
SELECT region, SUM(amount) AS total_amount, COUNT(*) AS order_count
FROM sales
GROUP BY region;
SELECT * FROM sales_by_region ORDER BY region;
