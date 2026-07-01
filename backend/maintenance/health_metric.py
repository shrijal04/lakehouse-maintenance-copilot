import os
import sys

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "spark"))

from spark.session import create_spark_session


class HealthService:

    def __init__(self, spark):
        self.spark = spark

    def get_table_health(self, table_name: str) -> dict:
        """
        Returns health metrics for an Iceberg table.
        """

        # ==========================================
        # Snapshot Count
        # ==========================================

        snapshot_count = self.spark.sql(f"""
            SELECT COUNT(*) AS snapshots
            FROM {table_name}.snapshots
        """).collect()[0]["snapshots"]

        # ==========================================
        # Data File Statistics
        # ==========================================

        files = self.spark.sql(f"""
            SELECT
                COUNT(*) AS file_count,
                ROUND(AVG(file_size_in_bytes) / 1024, 2) AS avg_file_kb,
                ROUND(SUM(file_size_in_bytes) / 1024 / 1024, 2) AS total_size_mb
            FROM {table_name}.files
        """).collect()[0]

        # ==========================================
        # Manifest Count
        # ==========================================

        manifest_count = self.spark.sql(f"""
            SELECT COUNT(*) AS manifest_count
            FROM {table_name}.all_manifests
        """).collect()[0]["manifest_count"]

        # ==========================================
        # Orphan Files
        # ==========================================

        orphan_file_count = 0

        return {
            "table": table_name,
            "snapshot_count": snapshot_count,
            "data_file_count": files["file_count"],
            "average_file_kb": files["avg_file_kb"],
            "total_size_mb": files["total_size_mb"],
            "manifest_file_count": manifest_count,
            "orphan_file_count": orphan_file_count,
        }

    def get_health_issues(self, metrics: dict):
        """
        Computes health issues based on table metrics.
        """

        issues = []

        # ==========================================
        # Snapshot Health
        # ==========================================

        if metrics["snapshot_count"] > 20:
            issues.append(
                {
                    "severity": "Warning",
                    "issue": "Too many snapshots",
                    "recommendation": "Run Expire Snapshots",
                }
            )

        # ==========================================
        # Small File Problem
        # ==========================================

        if metrics["average_file_kb"] < 512:
            issues.append(
                {
                    "severity": "Critical",
                    "issue": "Average file size is too small",
                    "recommendation": "Run Rewrite Data Files",
                }
            )

        # ==========================================
        # Metadata Health
        # ==========================================

        if metrics["manifest_file_count"] > 100:
            issues.append(
                {
                    "severity": "Warning",
                    "issue": "Large number of manifest files",
                    "recommendation": "Rewrite metadata",
                }
            )

        # ==========================================
        # Orphan Files
        # ==========================================

        if metrics["orphan_file_count"] > 0:
            issues.append(
                {
                    "severity": "Critical",
                    "issue": "Orphan files detected",
                    "recommendation": "Remove Orphan Files",
                }
            )

        # ==========================================
        # Healthy Table
        # ==========================================

        if not issues:
            issues.append(
                {
                    "severity": "Healthy",
                    "issue": "Table is healthy",
                    "recommendation": "No maintenance required",
                }
            )

        return issues

    def print_table_health(self, metrics: dict):
        """
        Prints a formatted health report.
        """

        print("=" * 60)
        print("Lakehouse Health Report")
        print("=" * 60)

        print(f"Table            : {metrics['table']}")
        print(f"Snapshots        : {metrics['snapshot_count']}")
        print(f"Manifest Files   : {metrics['manifest_file_count']}")
        print(f"Orphan Files     : {metrics['orphan_file_count']}")
        print(f"Data Files       : {metrics['data_file_count']}")
        print(f"Average File KB  : {metrics['average_file_kb']}")
        print(f"Total Size MB    : {metrics['total_size_mb']}")


def main():

    spark = create_spark_session()

    health_service = HealthService(spark)

    tables = [
        "local.lakehouse.orders",
        "local.lakehouse.order_items",
    ]

    for table in tables:

        metrics = health_service.get_table_health(table)

        health_service.print_table_health(metrics)

        print("\nDetected Issues")
        print("-" * 40)

        for issue in health_service.get_health_issues(metrics):
            print(issue)

        print("\n" + "=" * 60 + "\n")

    spark.stop()


if __name__ == "__main__":
    main()