import os

from dotenv import load_dotenv
from groq import Groq

from app.schemas.copilot import ChatMessage
from app.services.prompt_service import SYSTEM_PROMPT
from app.services.tool_service import ToolService

load_dotenv()


class AIService:

    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.tool_service = ToolService()

    def ask(
        self,
        messages: list[ChatMessage],
    ) -> str:

        if len(messages) == 0:
            return "Please ask a question."

        latest_question = messages[-1].content

        # -------------------------------------------------
        # Step 1 : Decide whether to use a tool
        # -------------------------------------------------

        if self.tool_service.should_use_tool(
            latest_question
        ):

            tool_result = self.tool_service.execute_tool(
                latest_question
            )

            if tool_result is not None:
                return tool_result

        # -------------------------------------------------
        # Step 2 : Build Conversation History
        # -------------------------------------------------

        conversation = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        for message in messages:
            conversation.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

        # -------------------------------------------------
        # Step 3 : Call Groq
        # -------------------------------------------------

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",

            messages=conversation,

            temperature=0.3,

            max_tokens=1024,
        )

        return response.choices[0].message.content