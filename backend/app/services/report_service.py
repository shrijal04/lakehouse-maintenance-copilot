from datetime import datetime
from statistics import mean

from app.repositories.report_repository import ReportRepository


class ReportService:

    def __init__(self):
        self.repository = ReportRepository()

    def build_today_report(self):

        health = self.repository.get_today_health()
        maintenance = self.repository.get_today_maintenance()
        etl_logs = self.repository.get_today_etl_logs()
        alerts = self.repository.get_today_alerts()

        health_scores = [
            h["health_score"]
            for h in health
            if h["health_score"] is not None
        ]

        average_health = (
            round(mean(health_scores), 2)
            if health_scores
            else 0
        )

        summary = {
            "tables_checked": len(
                set(h["table_name"] for h in health)
            ),
            "health_checks": len(health),
            "average_health_score": average_health,
            "maintenance_runs": len(maintenance),
            "etl_runs": len(etl_logs),
            "alerts": len(alerts),
        }

        return {
            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "summary": summary,
            "health": health,
            "maintenance": maintenance,
            "etl_logs": etl_logs,
            "alerts": alerts,
        }