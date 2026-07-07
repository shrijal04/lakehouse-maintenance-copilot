from datetime import datetime

from spark.config import POSTGRES
from spark.etl_repository import ETLRepository
from spark.manager import SparkManagerService
from spark.transformations import DataTransformer


class IncrementalETL:

    def __init__(self):

        self.spark = SparkManagerService().get_spark()

        self.repository = ETLRepository()

        self.transformer = DataTransformer()

    def run(self):

        start_time = datetime.now()

        # ==========================================================
        # Last Successful Run
        # ==========================================================

        last_run = self.repository.get_last_run(
            "orders_incremental"
        )

        print("=" * 60)
        print(f"Last Successful Run : {last_run}")
        print("=" * 60)

        # ==========================================================
        # Read Incremental Orders
        # ==========================================================

        orders_df = (
            self.spark.read
            .format("jdbc")
            .option("url", POSTGRES["url"])
            .option(
                "query",
                f"""
                SELECT *
                FROM orders
                WHERE updated_at > '{last_run}'
                """
            )
            .option("user", POSTGRES["user"])
            .option("password", POSTGRES["password"])
            .option("driver", POSTGRES["driver"])
            .load()
        )

        # ==========================================================
        # Read Incremental Order Items
        # ==========================================================

        order_items_df = (
            self.spark.read
            .format("jdbc")
            .option("url", POSTGRES["url"])
            .option(
                "query",
                f"""
                SELECT oi.*
                FROM order_items oi
                JOIN orders o
                    ON oi.order_id = o.order_id
                WHERE o.updated_at > '{last_run}'
                """
            )
            .option("user", POSTGRES["user"])
            .option("password", POSTGRES["password"])
            .option("driver", POSTGRES["driver"])
            .load()
        )

        orders_count = orders_df.count()
        items_count = order_items_df.count()

        print(f"Orders Found      : {orders_count}")
        print(f"Order Items Found : {items_count}")

        if orders_count == 0 and items_count == 0:

            print("No new records found.")

            return {
                "status": "No Changes",
                "orders_processed": 0,
                "order_items_processed": 0,
            }

        # ==========================================================
        # BRONZE LAYER
        # Raw data storage
        # ==========================================================

        print("\nUpdating Bronze Layer...")

        if orders_count > 0:

            (
                orders_df.writeTo(
                    "local.bronze.orders"
                )
                .append()
            )

            print("Bronze Orders Updated")

        if items_count > 0:

            (
                order_items_df.writeTo(
                    "local.bronze.order_items"
                )
                .append()
            )

            print("Bronze Order Items Updated")

        # ==========================================================
        # SILVER LAYER
        # Transformations
        # ==========================================================

        print("\nTransforming Data...")

        orders_df = (
            self.transformer.transform_orders(
                orders_df
            )
        )

        order_items_df = (
            self.transformer.transform_order_items(
                order_items_df
            )
        )

        # ==========================================================
        # SILVER MERGE - ORDERS
        # ==========================================================

        if orders_count > 0:

            orders_df.createOrReplaceTempView(
                "staging_orders"
            )

            with open(
                "spark/sql/merge_silver_orders.sql",
                "r",
            ) as f:

                merge_sql = f.read()

            self.spark.sql(merge_sql)

            print("Silver Orders Merged")

        # ==========================================================
        # SILVER MERGE - ORDER ITEMS
        # ==========================================================

        if items_count > 0:

            order_items_df.createOrReplaceTempView(
                "staging_order_items"
            )

            with open(
                "spark/sql/merge_silver_order_items.sql",
                "r",
            ) as f:

                merge_sql = f.read()

            self.spark.sql(merge_sql)

            print("Silver Order Items Merged")

        # ==========================================================
        # GOLD LAYER
        # Business Aggregations
        # ==========================================================

        print("\nRefreshing Gold Tables...")

        sql_files = [
            "spark/sql/refresh_daily_sales.sql",
            "spark/sql/refresh_store_sales.sql",
            "spark/sql/refresh_customer_sales.sql",
        ]

        for file in sql_files:

            with open(file, "r") as f:

                self.spark.sql(f.read())

        print("Gold Tables Refreshed")

        # ==========================================================
        # Update ETL Metadata
        # ==========================================================

        end_time = datetime.now()

        self.repository.update_last_run(
            "orders_incremental",
            end_time,
        )

        # ==========================================================
        # Save ETL Run History
        # ==========================================================

        self.repository.log_etl_run(
            pipeline_name="orders_incremental",
            start_time=start_time,
            end_time=end_time,
            status="SUCCESS",
            orders_processed=orders_count,
            order_items_processed=items_count,
            message="Bronze -> Silver -> Gold Incremental ETL Completed",
        )

        print("=" * 60)
        print("Incremental ETL Completed Successfully")
        print("=" * 60)

        print(f"Orders Processed      : {orders_count}")
        print(f"Order Items Processed : {items_count}")

        return {
            "status": "Success",
            "orders_processed": orders_count,
            "order_items_processed": items_count,
            "last_run": str(last_run),
        }


def main():

    pipeline = IncrementalETL()

    result = pipeline.run()

    print(result)


if __name__ == "__main__":

    main()