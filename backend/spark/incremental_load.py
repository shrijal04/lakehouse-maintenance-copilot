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
        # Last Successful ETL
        # ==========================================================

        last_run = self.repository.get_last_run(
            "orders_incremental"
        )

        print("=" * 60)
        print(f"Last successful run: {last_run}")
        print("=" * 60)

        # ==========================================================
        # Incremental Orders
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

        orders_df = self.transformer.transform_orders(orders_df)

        orders_count = orders_df.count()

        if orders_count > 0:

            orders_df.createOrReplaceTempView(
                "staging_orders"
            )

            with open(
                "spark/sql/merge_orders.sql",
                "r",
            ) as f:

                merge_sql = f.read()

            self.spark.sql(merge_sql)

            print("Orders merged successfully.")

        else:

            print("No changed orders found.")

        # ==========================================================
        # Incremental Order Items
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

        order_items_df = self.transformer.transform_order_items(
            order_items_df
        )

        items_count = order_items_df.count()

        if items_count > 0:

            order_items_df.createOrReplaceTempView(
                "staging_order_items"
            )

            with open(
                "spark/sql/merge_order_items.sql",
                "r",
            ) as f:

                merge_sql = f.read()

            self.spark.sql(merge_sql)

            print("Order items merged successfully.")

        else:

            print("No changed order items found.")

        # ==========================================================
        # Update Metadata
        # ==========================================================

        end_time = datetime.now()

        self.repository.update_last_run(
            "orders_incremental",
            end_time,
        )

        # ==========================================================
        # Save ETL Log
        # ==========================================================

        self.repository.log_etl_run(
            pipeline_name="orders_incremental",
            start_time=start_time,
            end_time=end_time,
            status="SUCCESS",
            orders_processed=orders_count,
            order_items_processed=items_count,
            message="Incremental load completed successfully.",
        )

        print("ETL metadata updated.")

        print("=" * 60)
        print(f"Changed orders      : {orders_count}")
        print(f"Changed order items : {items_count}")
        print("=" * 60)

        return {
            "status": "Success",
            "orders_merged": orders_count,
            "order_items_merged": items_count,
            "last_run": str(last_run),
        }


def main():

    pipeline = IncrementalETL()

    result = pipeline.run()

    print(result)


if __name__ == "__main__":

    main()