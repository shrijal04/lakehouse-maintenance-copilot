from datetime import datetime

from spark.manager import get_spark
from spark.config import POSTGRES
from spark.etl_repository import get_last_run, update_last_run
from spark.transformations import (
    transform_orders,
    transform_order_items,
)
from spark.etl_logs_repository import log_etl_run


def run_incremental_load():

    spark = get_spark()

    start_time = datetime.now()

    # ==========================================================
    # Last Successful ETL
    # ==========================================================

    last_run = get_last_run("orders_incremental")

    print("=" * 60)
    print(f"Last successful run: {last_run}")
    print("=" * 60)

    # ==========================================================
    # Incremental Orders
    # ==========================================================

    orders_df = (
        spark.read
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

    orders_df = transform_orders(orders_df)

    orders_count = orders_df.count()

    if orders_count > 0:

        orders_df.createOrReplaceTempView("staging_orders")

        with open("spark/sql/merge_orders.sql", "r") as f:
            merge_sql = f.read()

        spark.sql(merge_sql)

        print("Orders merged successfully.")

    else:

        print("No changed orders found.")

    # ==========================================================
    # Incremental Order Items
    # ==========================================================

    order_items_df = (
        spark.read
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

    order_items_df = transform_order_items(order_items_df)

    items_count = order_items_df.count()

    if items_count > 0:

        order_items_df.createOrReplaceTempView("staging_order_items")

        with open("spark/sql/merge_order_items.sql", "r") as f:
            merge_sql = f.read()

        spark.sql(merge_sql)

        print("Order items merged successfully.")

    else:

        print("No changed order items found.")

    # ==========================================================
    # Update ETL Metadata
    # ==========================================================

    end_time = datetime.now()

    update_last_run(
        "orders_incremental",
        end_time,
    )

    # ==========================================================
    # Save ETL Log
    # ==========================================================

    log_etl_run(
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

    # ----------------------------------------------------------
    # Do NOT stop Spark here.
    # FastAPI reuses the same Spark session for other endpoints.
    # ----------------------------------------------------------

    return {
        "status": "Success",
        "orders_merged": orders_count,
        "order_items_merged": items_count,
        "last_run": str(last_run),
    }


if __name__ == "__main__":

    result = run_incremental_load()

    print(result)