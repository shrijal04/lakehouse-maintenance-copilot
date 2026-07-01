import os
import sys

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "spark"))

from spark.session import SparkManager


class SmallFileGenerator:

    def __init__(self, spark, table_name):

        self.spark = spark
        self.table_name = table_name

    def configure_spark(self):

        # Disable adaptive merging
        self.spark.conf.set(
            "spark.sql.adaptive.enabled",
            "false",
        )

        # Force one partition
        self.spark.conf.set(
            "spark.sql.shuffle.partitions",
            "1",
        )

    def generate(self, batches=100):

        self.configure_spark()

        for i in range(batches):

            print(f"Writing batch {i + 1}/{batches}")

            (
                self.spark.table(self.table_name)
                .limit(5)
                .writeTo(self.table_name)
                .append()
            )

        print("\nFinished creating small files.")


def main():

    spark = SparkManager.get_spark()

    tables = [
        "local.lakehouse.orders",
        "local.lakehouse.order_items",
    ]

    for table in tables:

        print("=" * 60)
        print(f"Generating small files for {table}")
        print("=" * 60)

        generator = SmallFileGenerator(
            spark=spark,
            table_name=table,
        )

        generator.generate()

    spark.stop()


if __name__ == "__main__":
    main()