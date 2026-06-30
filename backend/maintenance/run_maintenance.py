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

TABLE = "local.lakehouse.orders"


def run_maintenance():

    # Shared Spark Session
    spark = get_spark()

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

    print("\nRewrite Manifest Files")
    manifest_df.show(truncate=False)

    # ===================================================
    # Expire Snapshots
    # ===================================================

    older_than = (
        datetime.now() - timedelta(hours=1)
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

    print("\nRemove Orphan Files")

    if orphan_df.count() == 0:
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
    # Improvement Summary
    # ===================================================

    snapshot_diff = before["snapshot_count"] - after["snapshot_count"]
    file_diff = before["data_file_count"] - after["data_file_count"]
    avg_diff = after["average_file_kb"] - before["average_file_kb"]
    size_diff = before["total_size_mb"] - after["total_size_mb"]

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

    return {
        "before": before,
        "rewrite_data_files": {
            "files_rewritten": rewrite.rewritten_data_files_count,
            "files_added": rewrite.added_data_files_count,
            "bytes_rewritten": rewrite.rewritten_bytes_count,
        },
        "rewrite_manifests": {
            "status": "completed"
        },
        "expire_snapshots": {
            column: getattr(expire, column)
            for column in expire_df.columns
        },
        "after": after,
    }


if __name__ == "__main__":
    run_maintenance()