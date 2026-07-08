from fastapi import APIRouter

from app.schemas.copilot import (
    ChatRequest,
    ChatResponse,
)

from app.services.ai_service import AIService
from app.services.ai_report_service import AIReportService

router = APIRouter(
    prefix="/copilot",
    tags=["Copilot"],
)

ai_service = AIService()
report_service = AIReportService()


@router.post(
    "/chat",
)
def chat(request: ChatRequest):

    # Get the user's latest message
    user_message = request.messages[-1].content.lower()

    # --------------------------------------------
    # If user asks for a report
    # --------------------------------------------

    report_keywords = [
        "report",
        "daily report",
        "generate report",
        "health report",
        "maintenance report",
    ]

    if any(keyword in user_message for keyword in report_keywords):

        report = report_service.generate_daily_report()

        return {
            "answer": report["summary"],
            "pdf": report["pdf"],
            "docx": report["docx"],
        }

    # --------------------------------------------
    # Otherwise use AI Copilot normally
    # --------------------------------------------

    answer = ai_service.ask(request.messages)

    return {
        "answer": answer,
    }