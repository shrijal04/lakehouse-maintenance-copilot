from sqlalchemy import text

from app.database import engine
from maintenance.health_metric import get_table_health
from spark.manager import get_spark

ORDERS_TABLE = "local.lakehouse.orders"
ORDER_ITEMS_TABLE = "local.lakehouse.order_items"


def get_dashboard_metrics():

    spark = get_spark()

    # =====================================================
    # Get health for both Iceberg tables
    # =====================================================

    orders = get_table_health(spark, ORDERS_TABLE)
    order_items = get_table_health(spark, ORDER_ITEMS_TABLE)

    # =====================================================
    # Combine metrics
    # =====================================================

    total_snapshots = (
        orders["snapshot_count"]
        + order_items["snapshot_count"]
    )

    total_storage = round(
        orders["total_size_mb"]
        + order_items["total_size_mb"],
        2,
    )

    combined_metrics = {
        "snapshot_count": total_snapshots,
        "average_file_kb": round(
            (
                orders["average_file_kb"]
                + order_items["average_file_kb"]
            )
            / 2,
            2,
        ),
        "manifest_file_count": (
            orders["manifest_file_count"]
            + order_items["manifest_file_count"]
        ),
        "orphan_file_count": (
            orders["orphan_file_count"]
            + order_items["orphan_file_count"]
        ),
    }

    with engine.connect() as conn:

        # =====================================================
        # Pipeline Activity
        # =====================================================

        pipeline_result = conn.execute(
            text("""
                SELECT
                    DATE(finished_at) AS day,
                    COUNT(*) AS jobs
                FROM maintenance_history
                GROUP BY DATE(finished_at)
                ORDER BY DATE(finished_at)
            """)
        )

        pipeline_activity = [
            {
                "day": str(row.day),
                "jobs": row.jobs,
            }
            for row in pipeline_result
        ]

        # =====================================================
        # Maintenance History (both tables)
        # =====================================================

        history_result = conn.execute(
            text("""
                SELECT
                    table_name,
                    finished_at,
                    status,
                    duration_seconds,
                    files_rewritten,
                    manifests_rewritten,
                    snapshots_deleted,
                    orphan_files_removed
                FROM maintenance_history
                WHERE table_name IN (:orders, :items)
                ORDER BY finished_at DESC
                LIMIT 20
            """),
            {
                "orders": ORDERS_TABLE,
                "items": ORDER_ITEMS_TABLE,
            },
        )

        maintenance_history = [
            {
                "table_name": row.table_name,
                "finished_at": row.finished_at,
                "status": row.status,
                "duration_seconds": row.duration_seconds,
                "files_rewritten": row.files_rewritten,
                "manifests_rewritten": row.manifests_rewritten,
                "snapshots_deleted": row.snapshots_deleted,
                "orphan_files_removed": row.orphan_files_removed,
            }
            for row in history_result
        ]

    return {
        "metrics": {
            "tables": 2,
            "snapshots": total_snapshots,
            "storage": total_storage,
            "healthScore": calculate_health_score(combined_metrics),
        },
        "pipelineActivity": pipeline_activity,
        "maintenanceHistory": maintenance_history,
    }


def calculate_health_score(metrics):

    score = 100

    if metrics["average_file_kb"] < 128:
        score -= 25

    if metrics["snapshot_count"] > 40:
        score -= 20

    if metrics["manifest_file_count"] > 200:
        score -= 15

    if metrics["orphan_file_count"] > 0:
        score -= 10

    return max(score, 0)