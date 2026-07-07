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

        # --------------------------------------------------
        # Create Bronze Namespace
        # --------------------------------------------------

        self.spark.sql(
            "CREATE NAMESPACE IF NOT EXISTS local.bronze"
        )

    def load_table(self, table_name: str):

        print("\n" + "=" * 60)
        print(f"Loading Bronze Table : {table_name}")
        print("=" * 60)

        # --------------------------------------------------
        # Read table from PostgreSQL
        # --------------------------------------------------

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

        print(f"Rows Loaded : {df.count()}")

        # --------------------------------------------------
        # Save as Bronze Iceberg Table
        # --------------------------------------------------

        (
            df.writeTo(
                f"local.bronze.{table_name}"
            )
            .using("iceberg")
            .createOrReplace()
        )

        print(
            f"Bronze table local.bronze.{table_name} created successfully."
        )

    def run(self):

        for table in self.TABLES:

            self.load_table(table)

        print("\nInitial Bronze Load Completed.")

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