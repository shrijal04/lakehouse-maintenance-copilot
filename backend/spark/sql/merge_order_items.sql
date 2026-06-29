MERGE INTO local.lakehouse.order_items AS target

USING staging_order_items AS source

ON target.item_id = source.item_id

WHEN MATCHED THEN
UPDATE SET
    target.order_id = source.order_id,
    target.product_id = source.product_id,
    target.quantity = source.quantity,
    target.unit_price = source.unit_price,
    target.discount = source.discount,
    target.line_total = source.line_total,
    target.created_at = source.created_at

WHEN NOT MATCHED THEN
INSERT (
    item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount,
    line_total,
    created_at
)
VALUES (
    source.item_id,
    source.order_id,
    source.product_id,
    source.quantity,
    source.unit_price,
    source.discount,
    source.line_total,
    source.created_at
);