from sqlalchemy import text

from app.database import engine


class ReportRepository:

    def __init__(self):
        self.engine = engine

    # ---------------------------------------------
    # Today's Health History
    # ---------------------------------------------
    def get_today_health(self):
        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT *
                    FROM lakehouse_health_history
                    WHERE DATE(recorded_at) = CURRENT_DATE
                    ORDER BY recorded_at ASC
                """)
            )

            return [dict(row._mapping) for row in result]

    # ---------------------------------------------
    # Today's Maintenance
    # ---------------------------------------------
    def get_today_maintenance(self):
        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT *
                    FROM maintenance_history
                    WHERE DATE(started_at) = CURRENT_DATE
                    ORDER BY started_at ASC
                """)
            )

            return [dict(row._mapping) for row in result]

    # ---------------------------------------------
    # Today's ETL Runs
    # ---------------------------------------------
    def get_today_etl_logs(self):
        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT *
                    FROM etl_logs
                    WHERE DATE(start_time) = CURRENT_DATE
                    ORDER BY start_time ASC
                """)
            )

            return [dict(row._mapping) for row in result]

    # ---------------------------------------------
    # Today's Alerts
    # ---------------------------------------------
    def get_today_alerts(self):
        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT *
                    FROM health_alerts
                    WHERE DATE(detected_at) = CURRENT_DATE
                    ORDER BY detected_at ASC
                """)
            )

            return [dict(row._mapping) for row in result]