from datetime import datetime

from spark.manager import SparkManagerService


class SmallFileSimulator:

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

    # --------------------------------------------------
    # Build selected tables
    # --------------------------------------------------

    def get_tables(
        self,
        catalog: str,
        database: str,
        target: str,
    ):

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

        tables = mapping.get(target.lower())

        if tables is None:
            raise ValueError(
                "target must be 'orders', 'order_items' or 'both'"
            )

        return tables

    # --------------------------------------------------
    # Simulate one table
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Run Simulation
    # --------------------------------------------------

    def run(
        self,
        database: str,
        target: str,
        batches: int = 100,
        rows_per_batch: int = 5,
        catalog: str = "local",
    ):

        """
        Creates small files in the selected Iceberg table(s).
        """

        self.configure_spark()

        tables = self.get_tables(
            catalog=catalog,
            database=database,
            target=target,
        )

        print("=" * 60)
        print("Simulating Small Files")
        print("=" * 60)

        summary = []

        for table in tables:

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
            "database": database,
            "target": target,
            "message": "Small files created successfully.",
            "tables": summary,
            "simulation_time": datetime.now().isoformat(),
        }


def main():

    simulator = SmallFileSimulator()

    result = simulator.run(
        database="lakehouse",
        target="both",
        batches=100,
    )

    print(result)


if __name__ == "__main__":
    main()