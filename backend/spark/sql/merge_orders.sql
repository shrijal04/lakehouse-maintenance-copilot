MERGE INTO local.lakehouse.orders AS target

USING staging_orders AS source

ON target.order_id = source.order_id

WHEN MATCHED THEN
UPDATE SET
    target.customer_id = source.customer_id,
    target.order_date = source.order_date,
    target.status = source.status,
    target.payment_method = source.payment_method,
    target.total_amount = source.total_amount,
    target.shipping_city = source.shipping_city,
    target.shipping_country = source.shipping_country,
    target.created_at = source.created_at,
    target.updated_at = source.updated_at,
    target.store_id = source.store_id

WHEN NOT MATCHED THEN
INSERT (
    order_id,
    customer_id,
    order_date,
    status,
    payment_method,
    total_amount,
    shipping_city,
    shipping_country,
    created_at,
    updated_at,
    store_id
)
VALUES (
    source.order_id,
    source.customer_id,
    source.order_date,
    source.status,
    source.payment_method,
    source.total_amount,
    source.shipping_city,
    source.shipping_country,
    source.created_at,
    source.updated_at,
    source.store_id
);