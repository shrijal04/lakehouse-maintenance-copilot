from sqlalchemy import text

from app.database import engine
from maintenance.health_metric import get_table_health
from spark.manager import get_spark


TABLE = "local.lakehouse.orders"


def get_dashboard_metrics():

    spark = get_spark()

    metrics = get_table_health(spark, TABLE)

    with engine.connect() as conn:

        pipeline = conn.execute(
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
            for row in pipeline
        ]

    return {
        "metrics": {
            "tables": 1,
            "snapshots": metrics["snapshot_count"],
            "storage": round(metrics["total_size_mb"], 2),
            "healthScore": calculate_health_score(metrics),
        },
        "pipelineActivity": pipeline_activity,
    }


def calculate_health_score(metrics):

    score = 100

    if metrics["average_file_kb"] < 128:
        score -= 25

    if metrics["snapshot_count"] > 20:
        score -= 20

    if metrics["manifest_file_count"] > 100:
        score -= 15

    return max(score, 0)