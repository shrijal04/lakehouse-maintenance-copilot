from app.tools.base_tool import BaseTool


class MaintenanceTool(BaseTool):
    """
    Placeholder for maintenance execution.

    Later this tool will request
    maintenance confirmation before
    executing Spark procedures.
    """

    def execute(
        self,
        database: str,
        table: str,
    ):

        return {
            "status": "pending",
            "message": (
                "Maintenance execution is not "
                "enabled yet."
            ),
            "database": database,
            "table": table,
        }