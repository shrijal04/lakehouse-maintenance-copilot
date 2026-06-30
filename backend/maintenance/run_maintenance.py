import os
import sys
from datetime import datetime, timedelta

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "spark"))

from spark.session import create_spark_session
from maintenance.health_metric import (
    get_table_health,
    print_table_health,
)


TABLE = "local.lakehouse.orders"


def run_maintenance():
    spark = create_spark_session()

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
        # Rewrite Small Files
        # ===================================================

        rewrite_df = spark.sql(f"""
        CALL local.system.rewrite_data_files(
            table => '{TABLE}'
        )
        """)

        print("\nRewrite Data Files Result")
        rewrite_df.show(truncate=False)

        rewrite = rewrite_df.first()

        print("\nSummary")
        print(f"Files rewritten : {rewrite.rewritten_data_files_count}")
        print(f"Files added     : {rewrite.added_data_files_count}")
        print(f"Bytes rewritten : {rewrite.rewritten_bytes_count}")

        if rewrite.rewritten_data_files_count == 0:
            print("Table is already optimized. No compaction required.")

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

        print("\nExpire Snapshots Result")
        expire_df.show(truncate=False)

        expire = expire_df.first()

        print("\nSummary")

        for column in expire_df.columns:
            print(f"{column}: {getattr(expire, column)}")

        # ===================================================
        # Remove Orphan Files
        # ===================================================

        orphan_df = spark.sql(f"""
        CALL local.system.remove_orphan_files(
            table => '{TABLE}'
        )
        """)

        orphan_count = orphan_df.count()

        print("\nRemove Orphan Files Result")

        if orphan_count == 0:
            print("No orphan files found.")
        else:
            orphan_df.show(truncate=False)

            orphan = orphan_df.first()

            print("\nSummary")

            for column in orphan_df.columns:
                print(f"{column}: {getattr(orphan, column)}")

        # ===================================================
        # After Maintenance
        # ===================================================

        print("\nAfter Maintenance\n")

        after = get_table_health(spark, TABLE)
        print_table_health(after)

        # ===================================================
        # Improvement Summary
        # ===================================================

        print("\n" + "=" * 60)
        print("Maintenance Improvement")
        print("=" * 60)

        snapshot_diff = before["snapshot_count"] - after["snapshot_count"]
        file_diff = before["data_file_count"] - after["data_file_count"]
        avg_diff = after["average_file_kb"] - before["average_file_kb"]
        size_diff = before["total_size_mb"] - after["total_size_mb"]

        print(
            f"Snapshots   : {before['snapshot_count']} -> {after['snapshot_count']} "
            f"({snapshot_diff} removed)"
        )

        print(
            f"Data Files  : {before['data_file_count']} -> {after['data_file_count']} "
            f"({file_diff} removed)"
        )

        print(
            f"Avg File KB : {before['average_file_kb']} -> {after['average_file_kb']} "
            f"({avg_diff:+.2f} KB)"
        )

        print(
            f"Total Size  : {before['total_size_mb']} MB -> {after['total_size_mb']} MB "
            f"({size_diff:.2f} MB reduced)"
        )

        print("=" * 60)
        print("Maintenance Finished")
        print("=" * 60)

        # ===================================================
        # Return Summary (Useful for FastAPI)
        # ===================================================

        return {
            "before": before,
            "rewrite": {
                "files_rewritten": rewrite.rewritten_data_files_count,
                "files_added": rewrite.added_data_files_count,
                "bytes_rewritten": rewrite.rewritten_bytes_count,
            },
            "expire_snapshots": {
                column: getattr(expire, column)
                for column in expire_df.columns
            },
            "after": after,
        }

    finally:
        spark.stop()


if __name__ == "__main__":
    run_maintenance()