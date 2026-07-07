CREATE OR REPLACE TABLE local.lakehouse.store_sales
USING iceberg AS

SELECT
    store_id,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_sales

FROM local.silver.orders

GROUP BY store_id;