from spark.manager import SparkManagerService
from spark.transformations import DataTransformer


class SilverInitialLoad:

    TABLES = [
        "orders",
        "order_items",
    ]

    def __init__(self):

        self.spark = SparkManagerService().get_spark()

        self.transformer = DataTransformer()

        self.spark.sql(
            "CREATE NAMESPACE IF NOT EXISTS local.silver"
        )

    def load_orders(self):

        print("\nLoading Silver Orders...")

        df = self.spark.table(
            "local.bronze.orders"
        )

        print(f"Rows: {df.count()}")

        df = self.transformer.transform_orders(df)

        (
            df.writeTo("local.silver.orders")
            .using("iceberg")
            .createOrReplace()
        )

        print("Silver Orders created successfully.")

    def load_order_items(self):

        print("\nLoading Silver Order Items...")

        df = self.spark.table(
            "local.bronze.order_items"
        )

        print(f"Rows: {df.count()}")

        df = self.transformer.transform_order_items(df)

        (
            df.writeTo("local.silver.order_items")
            .using("iceberg")
            .createOrReplace()
        )

        print("Silver Order Items created successfully.")

    def run(self):

        self.load_orders()

        self.load_order_items()

        print("\nSilver Initial Load Completed.")

        return {
            "status": "Success",
            "tables_loaded": 2,
        }


def main():

    pipeline = SilverInitialLoad()

    result = pipeline.run()

    

    print(result)


if __name__ == "__main__":

    main()