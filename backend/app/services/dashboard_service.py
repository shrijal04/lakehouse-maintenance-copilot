from sqlalchemy import text

from app.database import engine
from maintenance.health_metric import get_table_health
from spark.manager import get_spark

TABLE = "local.lakehouse.orders"


def get_dashboard_metrics():

    spark = get_spark()

    metrics = get_table_health(spark, TABLE)

    with engine.connect() as conn:

        # ==========================================
        # Pipeline Activity (Jobs per Day)
        # ==========================================

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

        # ==========================================
        # Maintenance History
        # ==========================================

        history_result = conn.execute(
            text("""
                SELECT
                    finished_at,
                    status,
                    duration_seconds,
                    files_rewritten,
                    manifests_rewritten,
                    snapshots_deleted,
                    orphan_files_removed
                FROM maintenance_history
                WHERE table_name = :table_name
                ORDER BY finished_at DESC
                LIMIT 10
            """),
            {
                "table_name": TABLE,
            },
        )

        maintenance_history = [
            {
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
            "tables": 1,
            "snapshots": metrics["snapshot_count"],
            "storage": round(metrics["total_size_mb"], 2),
            "healthScore": calculate_health_score(metrics),
        },
        "pipelineActivity": pipeline_activity,
        "maintenanceHistory": maintenance_history,
    }


def calculate_health_score(metrics):

    score = 100

    if metrics["average_file_kb"] < 128:
        score -= 25

    if metrics["snapshot_count"] > 20:
        score -= 20

    if metrics["manifest_file_count"] > 100:
        score -= 15

    if metrics["orphan_file_count"] > 0:
        score -= 10

    return max(score, 0)