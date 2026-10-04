-- @schema
CREATE TABLE monthly_sales (
    month TEXT PRIMARY KEY,
    revenue INTEGER NOT NULL
);
INSERT INTO monthly_sales VALUES ('2024-01', 1000);
INSERT INTO monthly_sales VALUES ('2024-02', 1200);
INSERT INTO monthly_sales VALUES ('2024-03', 900);
INSERT INTO monthly_sales VALUES ('2024-04', 1500);
-- @query
-- TODO: Return month, revenue and prev_revenue (the previous month's revenue, NULL for the first month), ordered by month.

