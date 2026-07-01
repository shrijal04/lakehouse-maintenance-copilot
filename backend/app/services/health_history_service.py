from sqlalchemy import text

from app.database import engine


class HealthRepository:

    def __init__(self):
        self.engine = engine

    # -------------------------------------------------
    # Save one health snapshot
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Return every recorded run
    # -------------------------------------------------

    def get_health_history(self, table_name: str):

        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT
                        id,
                        recorded_at,
                        snapshot_count,
                        data_file_count,
                        average_file_kb,
                        total_size_mb,
                        manifest_file_count,
                        orphan_file_count
                    FROM lakehouse_health_history
                    WHERE table_name = :table_nameLAKE
                    ORDER BY recorded_at ASC
                """),
                {
                    "table_name": table_name,
                },
            )

            history = []

            for run_no, row in enumerate(result, start=1):

                history.append(
                    {
                        "run": run_no,
                        "recorded_at": row.recorded_at.isoformat(),
                        "snapshot_count": row.snapshot_count,
                        "data_file_count": row.data_file_count,
                        "average_file_kb": float(row.average_file_kb),
                        "total_size_mb": float(row.total_size_mb),
                        "manifest_file_count": row.manifest_file_count,
                        "orphan_file_count": row.orphan_file_count,
                    }
                )

            return history