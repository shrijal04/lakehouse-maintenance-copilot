from pyspark.sql.functions import (
    upper,
    trim,
    col
)

def transform_orders(df):

    # Remove duplicate orders
    df = df.dropDuplicates(["order_id"])

    # Standardize status
    df = df.withColumn(
        "status",
        upper(trim(col("status")))
    )

    # Standardize payment method
    df = df.withColumn(
        "payment_method",
        trim(col("payment_method"))
    )

    # Replace missing shipping city
    df = df.fillna({
        "shipping_city": "Unknown"
    })

    # Remove invalid totals
    df = df.filter(
        col("total_amount") >= 0
    )

    return df

from pyspark.sql.functions import round


def transform_order_items(df):

    df = df.dropDuplicates(["item_id"])

    df = df.filter(
        col("quantity") > 0
    )

    df = df.filter(
        col("unit_price") > 0
    )

    df = df.withColumn(
        "line_total",
        round(
            col("quantity")
            * col("unit_price")
            * (1 - col("discount") / 100),
            2
        )
    )

    return df
