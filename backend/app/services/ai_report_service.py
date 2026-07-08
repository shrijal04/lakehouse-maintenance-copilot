from app.services.report_service import ReportService


class AIReportService:

    def __init__(self, llm):
        self.report_service = ReportService()
        self.llm = llm

    def generate_daily_report(self):

        report = self.report_service.build_today_report()

        return report