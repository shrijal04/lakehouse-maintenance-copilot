from app.services.conversation_service import (
    conversation_service,
)
from app.services.maintenance_service import (
    MaintenanceService,
)
from app.tools.base_tool import BaseTool


class MaintenanceTool(BaseTool):
    """
    Requests maintenance for an Iceberg table.

    The tool DOES NOT execute maintenance.
    Instead it creates a pending confirmation
    that the user must approve.
    """

    def __init__(self):

        self.maintenance_service = MaintenanceService()

    @property
    def name(self):

        return "maintenance"

    @property
    def description(self):

        return (
            "Requests maintenance for an "
            "Apache Iceberg table."
        )

    def execute(
        self,
        database: str,
        table: str,
    ):
        """
        Create a maintenance request.

        The request is stored inside the
        ConversationService so the AI can
        later understand 'Yes' or 'No'.
        """

        result = self.maintenance_service.request_maintenance(
            database=database,
            target=table,
        )

        # ---------------------------------------
        # Store pending confirmation
        # ---------------------------------------

        if result.get("confirmation_required"):

            conversation_service.set_pending_action(
                session_id="default",
                action={
                    "confirmation_id": result[
                        "confirmation_id"
                    ],
                    "database": database,
                    "table": table,
                    "action": "maintenance",
                },
            )

        return result