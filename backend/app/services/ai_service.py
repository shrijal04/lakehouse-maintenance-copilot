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
from app.services.alert_cache import CURRENT_ALERTS

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

                # Step 3 — route report-tool results to
                # their own prompt_type instead of falling
                # through to the generic "Health / Issues /
                # History" branch below.

                elif tool_name == "report":
                    prompt_type = "report"

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

        # -------------------------------------------------
        # Proactive Health Alerts
        # -------------------------------------------------

        if CURRENT_ALERTS:

            alert_text = "\n".join(
                [
                    (
                        f"Table: {alert['table']}\n"
                        f"Severity: {alert['severity']}\n"
                        f"Issue: {alert['issue']}\n"
                        f"Recommendation: {alert['recommendation']}"
                    )
                    for alert in CURRENT_ALERTS
                ]
            )

            conversation.append(
                {
                    "role": "system",
                    "content": f"""
        The lakehouse monitoring system has already detected the following active health issues.

        {alert_text}

        Before answering the user's question:

        - Briefly tell the user that a maintenance issue has already been detected.
        - Summarize the issue(s) in simple English.
        - Explain why they matter.
        - Mention the recommendation.
        - Then continue answering the user's actual question normally.

        Do NOT invent additional issues.
        Do NOT mention Spark internals.
        Do NOT mention implementation details.
        """,
                }
            )

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
Maintenance operation has completed.

Tool Output:

{tool_result}

Rules:

If status is "success":

Show:

# Maintenance Completed

## Operations Performed

## Summary

---------------------------------------

If status is "cancelled":

Explain that the maintenance request was cancelled.
No work was performed.

---------------------------------------

If status is "conflict":

Explain in very simple English.

Do NOT mention Java exceptions.

Do NOT show stack traces.

Explain that:

• Another user or process modified the table at the same time.

• Apache Iceberg protects the table by rejecting conflicting writes.

• No data was corrupted.

• The safest solution is simply to retry the maintenance.

End with:

"Your data remains safe."

---------------------------------------

Never generate SQL.

Never generate Spark code.

Never explain Iceberg internals.
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
        # Report Prompt (Step 4)
        # -------------------------------------------------

        elif (
            tool_result is not None
            and prompt_type == "report"
        ):

            conversation.append(
                {
                    "role": "system",
                    "content": f"""
Today's AI report has already been generated.

Tool Output

{tool_result}

Rules:

Show the report exactly.

Do not rewrite numbers.

Do not invent metrics.

At the end say:

"The report is ready to download."

Do not generate another report.
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

    def generate_daily_report(self, report: dict) -> str:

        conversation = [
            {
                "role": "system",
                "content": """
    You are a Senior Lakehouse Reliability Engineer.

    You are writing a professional Daily Lakehouse Incident Report.

    Use ONLY the provided data.

    Do not invent numbers.

    Keep the report easy to understand.

    The report must contain these sections.

    # Executive Summary

    # Lakehouse Health

    # Maintenance Activity

    # ETL Activity

    # Alerts

    # Overall Assessment

    # Recommendations
    """
            },
            {
                "role": "user",
                "content": str(report)
            }
        ]

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation,
            temperature=0.2,
            max_tokens=1500,
        )

        return response.choices[0].message.content