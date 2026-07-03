import json

from app.tools.base_tool import BaseTool
from app.services.maintenance_service import MaintenanceService


class HealthTool(BaseTool):

    def __init__(self):
        self.maintenance_service = MaintenanceService()

    def execute(
        self,
        database: str,
        table: str,
    ) -> str:

        result = self.maintenance_service.get_table_health(
            database=database,
            target=table,
        )

        # ------------------------------
        # Convert Pydantic models
        # into plain dictionaries
        # ------------------------------

        if isinstance(result, list):
            result = [
                item.model_dump()
                if hasattr(item, "model_dump")
                else item
                for item in result
            ]

        elif hasattr(result, "model_dump"):
            result = result.model_dump()

        # ------------------------------
        # Return formatted JSON string
        # ------------------------------

        return json.dumps(
            result,
            indent=2,
        )