from sqlalchemy import text

from app.database import engine


class HealthRepository:

    def __init__(self):
        self.engine = engine

    def save_health_metrics(self, metrics):

        with self.engine.begin() as conn:
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

    def get_health_history(self, table_name: str):

        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT
                        DATE(recorded_at) AS day,
                        AVG(snapshot_count) AS snapshot_count,
                        AVG(data_file_count) AS data_file_count,
                        AVG(average_file_kb) AS average_file_kb
                    FROM lakehouse_health_history
                    WHERE table_name = :table_name
                    GROUP BY DATE(recorded_at)
                    ORDER BY DATE(recorded_at)
                """),
                {
                    "table_name": table_name,
                },
            )

            return [
                {
                    "day": str(row.day),
                    "snapshot_count": round(row.snapshot_count),
                    "data_file_count": round(row.data_file_count),
                    "average_file_kb": round(row.average_file_kb, 2),
                }
                for row in result
            ]