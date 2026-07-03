import os

from dotenv import load_dotenv
from groq import Groq

from app.schemas.copilot import ChatMessage
from app.services.confirmation_parser import (
    ConfirmationParser,
)
from app.services.conversation_service import (
    conversation_service,
)
from app.services.maintenance_service import (
    MaintenanceService,
)
from app.services.prompt_service import SYSTEM_PROMPT
from app.services.tool_service import ToolService

load_dotenv()


class AIService:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.tool_service = ToolService()
        self.maintenance_service = MaintenanceService()
        self.confirmation_parser = ConfirmationParser()

    # -----------------------------------------------------

    def ask(
        self,
        messages: list[ChatMessage],
    ) -> str:

        if not messages:
            return "Please ask a question."

        latest_question = messages[-1].content.strip()

        tool_result = None
        prompt_type = "general"

        # -------------------------------------------------
        # Pending confirmation
        # -------------------------------------------------

        pending_action = (
            conversation_service.get_pending_action(
                session_id="default"
            )
        )

        if pending_action:

            if self.confirmation_parser.is_confirmation(
                latest_question
            ):

                tool_result = (
                    self.maintenance_service.confirm_maintenance(
                        confirmation_id=pending_action[
                            "confirmation_id"
                        ],
                        confirm=True,
                        database=pending_action[
                            "database"
                        ],
                        target=pending_action[
                            "table"
                        ],
                    )
                )

                conversation_service.clear_pending_action(
                    "default"
                )

                prompt_type = "maintenance_result"

            elif self.confirmation_parser.is_rejection(
                latest_question
            ):

                tool_result = (
                    self.maintenance_service.confirm_maintenance(
                        confirmation_id=pending_action[
                            "confirmation_id"
                        ],
                        confirm=False,
                        database=pending_action[
                            "database"
                        ],
                        target=pending_action[
                            "table"
                        ],
                    )
                )

                conversation_service.clear_pending_action(
                    "default"
                )

                prompt_type = "maintenance_result"

        # -------------------------------------------------
        # Execute tool
        # -------------------------------------------------

        elif self.tool_service.should_use_tool(
            latest_question
        ):

            try:

                tool_result = (
                    self.tool_service.execute_tool(
                        latest_question
                    )
                )

                tool_name = (
                    self.tool_service.detect_tool(
                        latest_question
                    )
                )

                if tool_name == "maintenance":
                    prompt_type = "maintenance_request"

                elif tool_name == "health":
                    prompt_type = "health"

                elif tool_name == "issues":
                    prompt_type = "issues"

                elif tool_name == "history":
                    prompt_type = "history"

            except Exception as e:

                print(e)

        # -------------------------------------------------
        # Conversation
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
        # Maintenance Request Prompt
        # -------------------------------------------------

        if (
            tool_result is not None
            and prompt_type == "maintenance_request"
        ):

            conversation.append(
                {
                    "role": "system",
                    "content": f"""
You are showing a maintenance confirmation.

Tool Output:

{tool_result}

Rules:

Do NOT explain Apache Iceberg.

Do NOT show SQL.

Do NOT provide code examples.

Do NOT repeat the user's question.

Simply show:

# Maintenance Request

• Database

• Table

• Operations that will run

Finally write ONLY:

Reply **Yes** to execute.

Reply **No** to cancel.
""",
                }
            )

        # -------------------------------------------------
        # Maintenance Result Prompt
        # -------------------------------------------------

        elif (
            tool_result is not None
            and prompt_type == "maintenance_result"
        ):

            conversation.append(
                {
                    "role": "system",
                    "content": f"""
Maintenance has already finished.

Tool Output:

{tool_result}

Rules:

Do NOT explain Iceberg.

Do NOT provide SQL.

Do NOT provide Spark examples.

Do NOT suggest commands.

Do NOT mention confirmations.

Summarize only the maintenance result.

Show:

# Maintenance Completed

## Before

## Operations Performed

## After

## Summary
""",
                }
            )

        # -------------------------------------------------
        # Health / Issues / History
        # -------------------------------------------------

        elif tool_result is not None:

            conversation.append(
                {
                    "role": "system",
                    "content": f"""
Live Tool Output

{tool_result}

Rules

Use ONLY this data.

Do NOT invent values.

Explain everything simply.

Use Markdown tables where appropriate.

Do not include SQL examples.

Do not include Spark code.

Do not mention internal implementation.
""",
                }
            )

        # -------------------------------------------------
        # Ask Groq
        # -------------------------------------------------

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation,
            temperature=0.2,
            max_tokens=1024,
        )

        return response.choices[0].message.content