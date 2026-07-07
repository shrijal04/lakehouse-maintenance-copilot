CREATE OR REPLACE TABLE local.lakehouse.daily_sales
USING iceberg AS

SELECT
    order_date,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_sales

FROM local.silver.orders

GROUP BY order_date;