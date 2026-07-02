from fastapi import APIRouter

from app.schemas.copilot import ChatRequest, ChatResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/copilot", tags=["Copilot"])

ai_service = AIService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = ai_service.ask(request.question)

    return ChatResponse(answer=answer)