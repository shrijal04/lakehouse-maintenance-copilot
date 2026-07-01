from spark.config import POSTGRES
from spark.manager import SparkManagerService


class InitialLoadPipeline:

    TABLES = [
        "customers",
        "products",
        "stores",
        "orders",
        "order_items",
    ]

    def __init__(self):

        self.spark = SparkManagerService().get_spark()

        self.spark.sql(
            "CREATE NAMESPACE IF NOT EXISTS local.lakehouse"
        )

    def load_table(self, table_name: str):

        print(f"\nLoading {table_name}...")

        df = (
            self.spark.read
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

    def run(self):

        for table in self.TABLES:

            self.load_table(table)

        print("\nInitial load completed.")

        return {
            "status": "Success",
            "tables_loaded": len(self.TABLES),
        }


def main():

    pipeline = InitialLoadPipeline()

    result = pipeline.run()

    print(result)


if __name__ == "__main__":

    main()