from datetime import datetime

from spark.manager import get_spark

TABLES = [
    "local.lakehouse.orders",
    "local.lakehouse.order_items",
]


def simulate_small_files(
    batches: int = 100,
    rows_per_batch: int = 5,
):
    """
    Intentionally creates the Iceberg small-file problem.

    For each Iceberg fact table, repeatedly appends a very small
    number of rows. This produces many tiny Parquet files and
    many snapshots for maintenance demonstrations.

    Duplicate rows are expected because this utility exists only
    to demonstrate Iceberg maintenance operations.
    """

    spark = get_spark()

    print("=" * 60)
    print("Simulating Small Files")
    print("=" * 60)

    # Disable adaptive execution so Spark does not merge writes.
    spark.conf.set(
        "spark.sql.adaptive.enabled",
        "false",
    )

    # Force a single shuffle partition.
    spark.conf.set(
        "spark.sql.shuffle.partitions",
        "1",
    )

    summary = []

    for table in TABLES:

        print()
        print("=" * 60)
        print(f"Creating small files for: {table}")
        print("=" * 60)

        for batch in range(batches):

            print(f"Batch {batch + 1}/{batches}")

            (
                spark.table(table)
                .limit(rows_per_batch)
                .writeTo(table)
                .append()
            )

        summary.append(
            {
                "table": table,
                "batches_written": batches,
                "rows_per_batch": rows_per_batch,
            }
        )

    print()
    print("=" * 60)
    print("Small File Simulation Completed")
    print("=" * 60)

    return {
        "status": "Success",
        "message": "Small files created successfully for all Iceberg fact tables.",
        "tables": summary,
        "simulation_time": datetime.now().isoformat(),
    }


if __name__ == "__main__":

    result = simulate_small_files()

    print(result)