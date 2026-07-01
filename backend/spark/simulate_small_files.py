from datetime import datetime

from spark.manager import SparkManagerService


class SmallFileSimulator:

    TABLES = [
        "local.lakehouse.orders",
        "local.lakehouse.order_items",
    ]

    def __init__(self):

        self.spark = SparkManagerService().get_spark()

    def configure_spark(self):

        # Disable adaptive execution
        self.spark.conf.set(
            "spark.sql.adaptive.enabled",
            "false",
        )

        # Force one shuffle partition
        self.spark.conf.set(
            "spark.sql.shuffle.partitions",
            "1",
        )

    def simulate_table(
        self,
        table: str,
        batches: int,
        rows_per_batch: int,
    ):

        print()
        print("=" * 60)
        print(f"Creating small files for: {table}")
        print("=" * 60)

        for batch in range(batches):

            print(f"Batch {batch + 1}/{batches}")

            (
                self.spark.table(table)
                .limit(rows_per_batch)
                .writeTo(table)
                .append()
            )

        return {
            "table": table,
            "batches_written": batches,
            "rows_per_batch": rows_per_batch,
        }

    def run(
        self,
        batches: int = 100,
        rows_per_batch: int = 5,
    ):

        """
        Intentionally creates the Iceberg small-file problem.

        Repeatedly appends very small batches to each Iceberg
        fact table, producing many tiny Parquet files and
        snapshots for maintenance demonstrations.
        """

        self.configure_spark()

        print("=" * 60)
        print("Simulating Small Files")
        print("=" * 60)

        summary = []

        for table in self.TABLES:

            summary.append(
                self.simulate_table(
                    table,
                    batches,
                    rows_per_batch,
                )
            )

        print()
        print("=" * 60)
        print("Small File Simulation Completed")
        print("=" * 60)

        return {
            "status": "Success",
            "message": (
                "Small files created successfully for all "
                "Iceberg fact tables."
            ),
            "tables": summary,
            "simulation_time": datetime.now().isoformat(),
        }


def main():

    simulator = SmallFileSimulator()

    result = simulator.run()

    print(result)


if __name__ == "__main__":

    main()