from pyspark.sql.functions import (
    upper,
    trim,
    col,
    round,
)


class DataTransformer:

    def transform_orders(self, df):

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

    def transform_order_items(self, df):

        # Remove duplicate items
        df = df.dropDuplicates(["item_id"])

        # Remove invalid quantities
        df = df.filter(
            col("quantity") > 0
        )

        # Remove invalid prices
        df = df.filter(
            col("unit_price") > 0
        )

        # Calculate line total
        df = df.withColumn(
            "line_total",
            round(
                col("quantity")
                * col("unit_price")
                * (1 - col("discount") / 100),
                2,
            )
        )

        return df