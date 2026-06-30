from sqlalchemy import text

from app.database import engine


def save_health_metrics(metrics):

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO lakehouse_health_history
                (
                    table_name,
                    snapshot_count,
                    data_file_count,
                    average_file_kb,
                    total_size_mb,
                    manifest_file_count,
                    orphan_file_count
                )
                VALUES
                (
                    :table,
                    :snapshot_count,
                    :data_file_count,
                    :average_file_kb,
                    :total_size_mb,
                    :manifest_file_count,
                    :orphan_file_count
                )
            """),
            {
                "table": metrics["table"],
                "snapshot_count": metrics["snapshot_count"],
                "data_file_count": metrics["data_file_count"],
                "average_file_kb": metrics["average_file_kb"],
                "total_size_mb": metrics["total_size_mb"],
                "manifest_file_count": metrics["manifest_file_count"],
                "orphan_file_count": metrics["orphan_file_count"],
            },
        )



def get_health_history(table_name: str):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT
                    recorded_at,
                    snapshot_count,
                    data_file_count,
                    average_file_kb
                FROM lakehouse_health_history
                WHERE table_name = :table
                ORDER BY recorded_at ASC
            """),
            {"table": table_name},
        )

        return [
            {
                "checked_at": row.recorded_at,
                "snapshot_count": row.snapshot_count,
                "data_file_count": row.data_file_count,
                "average_file_kb": row.average_file_kb,
            }
            for row in result
        ]