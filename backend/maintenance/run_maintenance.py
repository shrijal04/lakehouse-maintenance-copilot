import os
import sys
from datetime import datetime, timedelta

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "spark"))

from maintenance.health_metric import HealthService
from spark.manager import SparkManagerService

from app.services.maintenance_history_service import (
    MaintenanceHistoryRepository,
)


class Maintenance:

    def __init__(self, spark):

        self.spark = spark
        self.health_service = HealthService(spark)
        self.repo = MaintenanceHistoryRepository()

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
    # Maintain one table
    # --------------------------------------------------

    def maintain_table(self, table_name):

        print("\n" + "=" * 70)
        print(f"Maintaining Table : {table_name}")
        print("=" * 70)

        start_time = datetime.now()

        before = self.health_service.get_table_health(
            table_name
        )

        print("\nBefore Maintenance\n")
        self.health_service.print_table_health(before)

        # ==========================================
        # Rewrite Data Files
        # ==========================================

        rewrite_df = self.spark.sql(f"""
            CALL local.system.rewrite_data_files(
                table => '{table_name}'
            )
        """)

        rewrite = rewrite_df.first()

        print("\nRewrite Data Files")
        rewrite_df.show(truncate=False)

        # ==========================================
        # Rewrite Manifests
        # ==========================================

        manifest_df = self.spark.sql(f"""
            CALL local.system.rewrite_manifests(
                table => '{table_name}'
            )
        """)

        manifest = manifest_df.first()

        print("\nRewrite Manifest Files")
        manifest_df.show(truncate=False)

        # ==========================================
        # Expire Snapshots
        # ==========================================

        older_than = (
            datetime.now() - timedelta(minutes=1)
        ).strftime("%Y-%m-%d %H:%M:%S")

        expire_df = self.spark.sql(f"""
            CALL local.system.expire_snapshots(
                table => '{table_name}',
                older_than => TIMESTAMP '{older_than}',
                retain_last => 5
            )
        """)

        expire = expire_df.first()

        print("\nExpire Snapshots")
        expire_df.show(truncate=False)

        # ==========================================
        # Remove Orphan Files
        # ==========================================

        orphan_df = self.spark.sql(f"""
            CALL local.system.remove_orphan_files(
                table => '{table_name}'
            )
        """)

        orphan_files_removed = orphan_df.count()

        print("\nRemove Orphan Files")

        if orphan_files_removed == 0:
            print("No orphan files found.")
        else:
            orphan_df.show(truncate=False)

        # ==========================================
        # After Maintenance
        # ==========================================

        after = self.health_service.get_table_health(
            table_name
        )

        print("\nAfter Maintenance\n")
        self.health_service.print_table_health(after)

        end_time = datetime.now()

        duration = int(
            (end_time - start_time).total_seconds()
        )

        self.repo.save_maintenance_job(
            {
                "table_name": table_name,
                "status": "Success",
                "duration_seconds": duration,
                "files_rewritten": rewrite.rewritten_data_files_count,
                "files_added": rewrite.added_data_files_count,
                "bytes_rewritten": rewrite.rewritten_bytes_count,
                "manifests_rewritten": manifest.rewritten_manifests_count,
                "manifests_added": manifest.added_manifests_count,
                "snapshots_deleted": expire.deleted_data_files_count,
                "manifest_files_deleted": expire.deleted_manifest_files_count,
                "manifest_lists_deleted": expire.deleted_manifest_lists_count,
                "orphan_files_removed": orphan_files_removed,
            }
        )

        return {
            "table": table_name,
            "before": before,
            "rewrite_data_files": {
                "files_rewritten": rewrite.rewritten_data_files_count,
                "files_added": rewrite.added_data_files_count,
                "bytes_rewritten": rewrite.rewritten_bytes_count,
            },
            "rewrite_manifests": {
                "manifests_rewritten": manifest.rewritten_manifests_count,
                "manifests_added": manifest.added_manifests_count,
            },
            "expire_snapshots": {
                column: getattr(expire, column)
                for column in expire_df.columns
            },
            "after": after,
        }

    # --------------------------------------------------
    # Run Maintenance
    # --------------------------------------------------

    def run_maintenance(
        self,
        database: str,
        target: str,
        catalog: str = "local",
    ):

        tables = self.get_tables(
            catalog=catalog,
            database=database,
            target=target,
        )

        results = []

        for table in tables:

            results.append(
                self.maintain_table(table)
            )

        return {
            "status": "Success",
            "database": database,
            "target": target,
            "tables": results,
        }


def main():

    spark = SparkManagerService().get_spark()

    maintenance = Maintenance(spark)

    result = maintenance.run_maintenance(
        database="lakehouse",
        target="both",
    )

    print(result)

    spark.stop()


if __name__ == "__main__":
    main()