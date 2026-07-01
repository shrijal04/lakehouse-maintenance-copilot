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

TABLES = [
    "local.lakehouse.orders",
    "local.lakehouse.order_items",
]


def maintain_table(spark, table_name):

    print("\n" + "=" * 70)
    print(f"Maintaining Table : {table_name}")
    print("=" * 70)

    start_time = datetime.now()

    before = get_table_health(spark, table_name)

    print("\nBefore Maintenance\n")
    print_table_health(before)

    # ===================================================
    # Rewrite Data Files
    # ===================================================

    rewrite_df = spark.sql(f"""
    CALL local.system.rewrite_data_files(
        table => '{table_name}'
    )
    """)

    rewrite = rewrite_df.first()

    print("\nRewrite Data Files")
    rewrite_df.show(truncate=False)

    # ===================================================
    # Rewrite Manifests
    # ===================================================

    manifest_df = spark.sql(f"""
    CALL local.system.rewrite_manifests(
        table => '{table_name}'
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
        table => '{table_name}',
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
        table => '{table_name}'
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

    after = get_table_health(spark, table_name)

    print("\nAfter Maintenance\n")
    print_table_health(after)

    # ===================================================
    # Summary
    # ===================================================

    print("\n" + "=" * 60)
    print(f"Maintenance Summary : {table_name}")
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

    end_time = datetime.now()

    duration = int(
        (end_time - start_time).total_seconds()
    )

    # ===================================================
    # Save Maintenance History
    # ===================================================

    save_maintenance_job(
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


def run_maintenance():

    spark = get_spark()

    results = []

    try:

        for table in TABLES:
            results.append(
                maintain_table(
                    spark,
                    table,
                )
            )

        return {
            "status": "Success",
            "tables": results,
        }

    except Exception:

        raise


if __name__ == "__main__":

    result = run_maintenance()

    print(result)