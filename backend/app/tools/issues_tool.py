from app.services.maintenance_service import MaintenanceService
from app.tools.base_tool import BaseTool


class IssuesTool(BaseTool):
    """
    Retrieves health issues for one or more
    Iceberg tables.
    """

    def __init__(self):
        self.maintenance_service = MaintenanceService()

    @property
    def name(self):
        return "issues"

    @property
    def description(self):
        return "Returns health issues for Iceberg tables."

    def execute(
        self,
        database: str,
        table: str,
    ):

        return self.maintenance_service.get_table_issues(
            database=database,
            target=table,
        )