from spark.manager import SparkManagerService
from spark.transformations import DataTransformer


class SilverDimensionPipeline:

    TABLES = [
        "customers",
        "products",
        "stores",
    ]

    def __init__(self):

        self.spark = SparkManagerService().get_spark()

        self.transformer = DataTransformer()

        self.spark.sql(
            "CREATE NAMESPACE IF NOT EXISTS local.silver"
        )

    # =====================================================
    # Load one dimension table
    # =====================================================

    def load_table(self, table_name):

        print("=" * 60)
        print(f"Loading {table_name}")
        print("=" * 60)

        df = self.spark.table(
            f"local.bronze.{table_name}"
        )

        print(f"Rows Read : {df.count()}")

        # -------------------------------------
        # Transform
        # -------------------------------------

        if table_name == "customers":

            df = self.transformer.transform_customers(df)

        elif table_name == "products":

            df = self.transformer.transform_products(df)

        elif table_name == "stores":

            df = self.transformer.transform_stores(df)

        # -------------------------------------
        # Save to Silver
        # -------------------------------------

        (
            df.writeTo(
                f"local.silver.{table_name}"
            )
            .using("iceberg")
            .createOrReplace()
        )

        print(
            f"Silver table local.silver.{table_name} created."
        )

    # =====================================================
    # Run Pipeline
    # =====================================================

    def run(self):

        for table in self.TABLES:

            self.load_table(table)

        print("\nSilver Dimension Load Completed.")

        return {
            "status": "Success",
            "tables_loaded": len(self.TABLES),
        }


def main():

    pipeline = SilverDimensionPipeline()

    result = pipeline.run()

    print(result)


if __name__ == "__main__":

    main()