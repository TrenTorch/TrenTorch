SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_revenue FROM monthly_sales ORDER BY month;
