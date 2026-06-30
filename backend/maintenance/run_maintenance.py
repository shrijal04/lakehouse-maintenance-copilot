import os
import sys
from datetime import datetime, timedelta

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "spark"))

from spark.manager import get_spark

from maintenance.health_metric import (
    get_table_health,
    print_table_health,
)

from app.services.maintenance_history_service import (
    save_maintenance_job,
)

TABLE = "local.lakehouse.orders"


def run_maintenance():

    spark = get_spark()

    start_time = datetime.now()

    try:

        # ===================================================
        # Before Maintenance
        # ===================================================

        print("\nBefore Maintenance\n")

        before = get_table_health(spark, TABLE)
        print_table_health(before)

        print("=" * 60)
        print("Running Iceberg Maintenance")
        print("=" * 60)

        # ===================================================
        # Rewrite Data Files
        # ===================================================

        rewrite_df = spark.sql(f"""
        CALL local.system.rewrite_data_files(
            table => '{TABLE}'
        )
        """)

        rewrite = rewrite_df.first()

        print("\nRewrite Data Files")
        rewrite_df.show(truncate=False)

        # ===================================================
        # Rewrite Manifest Files
        # ===================================================

        manifest_df = spark.sql(f"""
        CALL local.system.rewrite_manifests(
            table => '{TABLE}'
        )
        """)

        manifest = manifest_df.first()

        print("\nRewrite Manifest Files")
        manifest_df.show(truncate=False)

        # ===================================================
        # Expire Snapshots
        # ===================================================

        older_than = (
            datetime.now() - timedelta(minutes=1)
        ).strftime("%Y-%m-%d %H:%M:%S")

        expire_df = spark.sql(f"""
        CALL local.system.expire_snapshots(
            table => '{TABLE}',
            older_than => TIMESTAMP '{older_than}',
            retain_last => 5
        )
        """)

        expire = expire_df.first()

        print("\nExpire Snapshots")
        expire_df.show(truncate=False)

        # ===================================================
        # Remove Orphan Files
        # ===================================================

        orphan_df = spark.sql(f"""
        CALL local.system.remove_orphan_files(
            table => '{TABLE}'
        )
        """)

        orphan_files_removed = orphan_df.count()

        print("\nRemove Orphan Files")

        if orphan_files_removed == 0:
            print("No orphan files found.")
        else:
            orphan_df.show(truncate=False)

        # ===================================================
        # After Maintenance
        # ===================================================

        print("\nAfter Maintenance\n")

        after = get_table_health(spark, TABLE)
        print_table_health(after)

        # ===================================================
        # Summary
        # ===================================================

        print("\n" + "=" * 60)
        print("Maintenance Summary")
        print("=" * 60)

        print(
            f"Snapshots   : {before['snapshot_count']} -> {after['snapshot_count']}"
        )

        print(
            f"Data Files  : {before['data_file_count']} -> {after['data_file_count']}"
        )

        print(
            f"Avg File KB : {before['average_file_kb']} -> {after['average_file_kb']}"
        )

        print(
            f"Total Size  : {before['total_size_mb']} MB -> {after['total_size_mb']} MB"
        )

        print("=" * 60)

        # ===================================================
        # Save Maintenance History
        # ===================================================

        end_time = datetime.now()

        duration = int(
            (end_time - start_time).total_seconds()
        )

        save_maintenance_job(
            {
                "table_name": TABLE,
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

        # ===================================================
        # Return API Response
        # ===================================================

        return {
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

    except Exception:

        end_time = datetime.now()

        duration = int(
            (end_time - start_time).total_seconds()
        )

        save_maintenance_job(
            {
                "table_name": TABLE,
                "status": "Failed",
                "duration_seconds": duration,

                "files_rewritten": 0,
                "files_added": 0,
                "bytes_rewritten": 0,

                "manifests_rewritten": 0,
                "manifests_added": 0,

                "snapshots_deleted": 0,
                "manifest_files_deleted": 0,
                "manifest_lists_deleted": 0,

                "orphan_files_removed": 0,
            }
        )

        raise