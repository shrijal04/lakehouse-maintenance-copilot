from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
)

from reportlab.lib.styles import getSampleStyleSheet


class PDFGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

        Path("reports/generated").mkdir(
            parents=True,
            exist_ok=True,
        )

    def generate(
        self,
        ai_report: str,
    ):

        pdf_path = (
            "reports/generated/daily_report.pdf"
        )

        doc = SimpleDocTemplate(pdf_path)

        content = []

        content.append(
            Paragraph(
                "Lakehouse Daily Incident Report",
                self.styles["Title"],
            )
        )

        content.append(Spacer(1, 20))

        content.append(
            Paragraph(
                ai_report.replace("\n", "<br/>"),
                self.styles["BodyText"],
            )
        )

        chart_folder = Path("reports/charts")

        charts = [
            "health_score.png",
            "snapshots.png",
            "data_files.png",
            "average_file_size.png",
            "storage.png",
        ]

        for chart in charts:

            chart_path = chart_folder / chart

            if chart_path.exists():

                content.append(Spacer(1, 20))

                content.append(
                    Image(
                        str(chart_path),
                        width=450,
                        height=250,
                    )
                )

        doc.build(content)

        return pdf_path