from session import create_spark_session
from config import POSTGRES

spark = create_spark_session()

spark.sql("CREATE NAMESPACE IF NOT EXISTS local.lakehouse")


def load_table(table_name: str):

    print(f"\nLoading {table_name}...")

    df = (
        spark.read
        .format("jdbc")
        .option("url", POSTGRES["url"])
        .option("dbtable", table_name)
        .option("user", POSTGRES["user"])
        .option("password", POSTGRES["password"])
        .option("driver", POSTGRES["driver"])
        .load()
    )

    print(f"Rows: {df.count()}")

    (
        df.writeTo(f"local.lakehouse.{table_name}")
        .using("iceberg")
        .createOrReplace()
    )

    print(f"{table_name} loaded successfully.")


TABLES = [
    "customers",
    "products",
    "stores",
    "orders",
    "order_items"
]


for table in TABLES:
    load_table(table)

print("\nInitial load completed.")

spark.stop()