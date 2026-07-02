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

        # Disable adaptive execution
        self.spark.conf.set(
            "spark.sql.adaptive.enabled",
            "false",
        )

        # Force one output partition
        self.spark.conf.set(
            "spark.sql.shuffle.partitions",
            "1",
        )

    def generate(self, batches=100):

        self.configure_spark()

        for i in range(batches):

            print(
                f"Writing batch {i + 1}/{batches} "
                f"into {self.table_name}"
            )

            (
                self.spark.table(self.table_name)
                .limit(5)
                .writeTo(self.table_name)
                .append()
            )

        print(f"\nFinished creating small files for {self.table_name}")


def get_tables(catalog, database, target):
    """
    Returns the list of tables to simulate.
    """

    base = f"{catalog}.{database}"

    mapping = {
        "orders": [
            f"{base}.orders",
        ],
        "order_items": [
            f"{base}.order_items",
        ],
        "both": [
            f"{base}.orders",
            f"{base}.order_items",
        ],
    }

    return mapping.get(target.lower(), [])


def simulate_small_files(
    catalog,
    database,
    target,
    batches=100,
):

    spark = SparkManager.get_spark()

    tables = get_tables(
        catalog=catalog,
        database=database,
        target=target,
    )

    if not tables:
        raise ValueError(
            "target must be 'orders', 'order_items', or 'both'"
        )

    for table in tables:

        print("=" * 60)
        print(f"Generating small files for {table}")
        print("=" * 60)

        generator = SmallFileGenerator(
            spark=spark,
            table_name=table,
        )

        generator.generate(
            batches=batches
        )

    spark.stop()


def main():

    simulate_small_files(
        catalog="local",
        database="lakehouse",
        target="both",
        batches=100,
    )


if __name__ == "__main__":
    main()