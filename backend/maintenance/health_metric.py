import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "spark"))

from spark.session import create_spark_session


def get_table_health(spark, table_name: str) -> dict:
    """
    Returns health metrics for an Iceberg table.
    """

    snapshot_count = spark.sql(f"""
        SELECT COUNT(*) AS snapshots
        FROM {table_name}.snapshots
    """).collect()[0]["snapshots"]

    files = spark.sql(f"""
        SELECT
            COUNT(*) AS file_count,
            ROUND(AVG(file_size_in_bytes) / 1024, 2) AS avg_file_kb,
            ROUND(SUM(file_size_in_bytes) / 1024 / 1024, 2) AS total_size_mb
        FROM {table_name}.files
    """).collect()[0]

    return {
        "table": table_name,
        "snapshot_count": snapshot_count,
        "data_file_count": files["file_count"],
        "average_file_kb": files["avg_file_kb"],
        "total_size_mb": files["total_size_mb"],
    }


def print_table_health(metrics: dict):
    """
    Pretty prints table health.
    """

    print("=" * 60)
    print("Lakehouse Health Report")
    print("=" * 60)

    print(f"Table           : {metrics['table']}")
    print(f"Snapshots       : {metrics['snapshot_count']}")
    print(f"Data Files      : {metrics['data_file_count']}")
    print(f"Average File KB : {metrics['average_file_kb']}")
    print(f"Total Size MB   : {metrics['total_size_mb']}")


if __name__ == "__main__":
    spark = create_spark_session()

    TABLE = "local.lakehouse.orders"

    metrics = get_table_health(spark, TABLE)
    print_table_health(metrics)

    spark.stop()