from app.services.maintenance_service import MaintenanceService
from app.tools.base_tool import BaseTool


class HistoryTool(BaseTool):
    """
    Retrieves historical health metrics
    for one or more Iceberg tables.
    """

    def __init__(self):
        self.maintenance_service = MaintenanceService()

    def execute(
        self,
        database: str,
        table: str,
    ):

        return self.maintenance_service.get_table_health_history(
            database=database,
            target=table,
        )