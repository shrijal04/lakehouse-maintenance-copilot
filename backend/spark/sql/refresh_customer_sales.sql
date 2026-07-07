CREATE OR REPLACE TABLE local.lakehouse.customer_sales
USING iceberg AS

SELECT
    customer_id,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_sales

FROM local.silver.orders

GROUP BY customer_id;