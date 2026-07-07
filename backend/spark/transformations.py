from pyspark.sql.functions import (
    upper,
    trim,
    col,
    round,
    initcap,
)


class DataTransformer:

    # ==========================================================
    # Customers
    # ==========================================================

    def transform_customers(self, df):

        df = df.dropDuplicates(["customer_id"])

        df = df.withColumn(
            "first_name",
            initcap(trim(col("first_name")))
        )

        df = df.withColumn(
            "last_name",
            initcap(trim(col("last_name")))
        )

        df = df.withColumn(
            "email",
            trim(col("email"))
        )

        df = df.withColumn(
            "city",
            initcap(trim(col("city")))
        )

        df = df.withColumn(
            "country",
            initcap(trim(col("country")))
        )

        df = df.withColumn(
            "customer_segment",
            upper(trim(col("customer_segment")))
        )

        df = df.filter(
            col("email").isNotNull()
        )

        return df

    # ==========================================================
    # Products
    # ==========================================================

    def transform_products(self, df):

        df = df.dropDuplicates(["product_id"])

        df = df.withColumn(
            "product_name",
            trim(col("product_name"))
        )

        df = df.filter(
            col("price") >= 0
        )

        df = df.filter(
            col("stock_quantity") >= 0
        )

        return df

    # ==========================================================
    # Stores
    # ==========================================================

    def transform_stores(self, df):

        df = df.dropDuplicates(["store_id"])

        df = df.withColumn(
            "store_name",
            trim(col("store_name"))
        )

        df = df.withColumn(
            "city",
            initcap(trim(col("city")))
        )

        df = df.withColumn(
            "country",
            initcap(trim(col("country")))
        )

        df = df.withColumn(
            "manager_name",
            initcap(trim(col("manager_name")))
        )

        return df

    # ==========================================================
    # Orders
    # ==========================================================

    def transform_orders(self, df):

        df = df.dropDuplicates(["order_id"])

        df = df.withColumn(
            "status",
            upper(trim(col("status")))
        )

        df = df.withColumn(
            "payment_method",
            trim(col("payment_method"))
        )

        df = df.fillna({
            "shipping_city": "Unknown"
        })

        df = df.filter(
            col("total_amount") >= 0
        )

        return df

    # ==========================================================
    # Order Items
    # ==========================================================

    def transform_order_items(self, df):

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
                2,
            )
        )

        return df