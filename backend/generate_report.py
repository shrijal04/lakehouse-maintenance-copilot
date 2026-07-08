from app.services.report_service import ReportService
from app.services.ai_service import AIService

from app.reports.chart_generator import (
    ChartGenerator,
)

from app.reports.pdf_generator import (
    PDFGenerator,
)

print("Building report...")

report = ReportService().build_today_report()

print("Generating AI summary...")

ai_report = AIService().generate_daily_report(
    report
)

print("Generating charts...")

ChartGenerator().generate_all()

print("Generating PDF...")

pdf = PDFGenerator().generate(ai_report)

print(f"Done: {pdf}")