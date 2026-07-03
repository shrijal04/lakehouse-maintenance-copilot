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

        if not messages:
            return "Please ask a question."

        latest_question = messages[-1].content

        # -------------------------------------------------
        # Execute backend tool if required
        # -------------------------------------------------

        tool_result = None

        if self.tool_service.should_use_tool(
            latest_question
        ):
            try:
                tool_result = self.tool_service.execute_tool(
                    latest_question
                )
            except Exception as e:
                print(f"Tool Error: {e}")

        # -------------------------------------------------
        # Build conversation
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
        # Inject live tool result
        # -------------------------------------------------

        if tool_result is not None:

            conversation.append(
                {
                    "role": "system",
                    "content": f"""
The following information was retrieved LIVE from the user's Apache Iceberg lakehouse.

Live Data
---------
{tool_result}

Instructions:
- Use this live information when answering.
- Treat these values as the source of truth.
- Do NOT invent or estimate values.
- Explain the results in simple language.
- If maintenance is recommended, explain why.
- If everything looks healthy, mention that as well.
""",
                }
            )

        # -------------------------------------------------
        # Call Groq
        # -------------------------------------------------

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation,
            temperature=0.3,
            max_tokens=1024,
        )

        return response.choices[0].message.content