import os

from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from app.services.report_service import ReportService
from app.services.report_export_service import ReportExportService
from app.reports.chart_generator import ChartGenerator

load_dotenv()


class AIReportService:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.report_service = ReportService()
        self.export_service = ReportExportService()
        self.chart_generator = ChartGenerator()

    # --------------------------------------------------
    # Generate AI Daily Report
    # --------------------------------------------------

    def generate_daily_report(self):

        # -----------------------------
        # Build today's report data
        # -----------------------------

        report = self.report_service.build_today_report()

        # -----------------------------
        # Generate charts
        # -----------------------------

        self.chart_generator.generate_all()

        # -----------------------------
        # AI Prompt
        # -----------------------------

        prompt = f"""
You are a Lakehouse Maintenance Assistant.

Write a professional daily report.

Use simple English.

Include the following sections:

# Executive Summary

# Lakehouse Health

# Maintenance Activity

# ETL Activity

# Alerts

# Overall Assessment

# Recommendations

Today's Lakehouse Data:

{report}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        report_text = response.choices[0].message.content

        # -----------------------------
        # Export PDF
        # -----------------------------

        pdf_path = self.export_service.export_pdf(
            title="Lakehouse Daily Report",
            report_text=report_text,
        )

        # -----------------------------
        # Export DOCX
        # -----------------------------

        docx_path = self.export_service.export_docx(
            title="Lakehouse Daily Report",
            report_text=report_text,
        )

        # -----------------------------
        # Return only filenames (Step 5)
        # -----------------------------

        return {
            "summary": report_text,
            "pdf": Path(pdf_path).name,
            "docx": Path(docx_path).name,
        }