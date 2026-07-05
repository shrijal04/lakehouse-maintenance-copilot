from app.services.maintenance_service import MaintenanceService


class MaintenanceTool:

    def __init__(self):
        self.maintenance_service = MaintenanceService()

    def execute(
        self,
        database: str,
        table: str,
        confirm: bool = False,
    ):
        """
        Execute maintenance on an Iceberg table.

        Parameters
        ----------
        database : str
            Database name.

        table : str
            Target table.

        confirm : bool
            Maintenance only runs when this is True.
        """

        if not confirm:
            return {
                "status": "confirmation_required",
                "message": (
                    "Maintenance requires confirmation. "
                    "Call this tool again with confirm=True."
                ),
            }

        return self.maintenance_service.run_maintenance(
            database=database,
            target=table,
        )