from sqlalchemy import text

from app.database import engine


class ChartRepository:

    def __init__(self):
        self.engine = engine

    def get_health_history(self):

        with self.engine.connect() as conn:

            rows = conn.execute(
                text("""
                SELECT
                    recorded_at,
                    table_name,
                    health_score,
                    snapshot_count,
                    data_file_count,
                    average_file_kb,
                    total_size_mb
                FROM lakehouse_health_history
                ORDER BY recorded_at
                """)
            )

            return [dict(row._mapping) for row in rows]