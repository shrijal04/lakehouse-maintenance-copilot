from fastmcp import FastMCP

from app.services.maintenance_service import (
    MaintenanceService,
)


def register_history_tool(
    mcp: FastMCP,
):
    """
    Register the Lakehouse Health History Tool
    with the MCP server.
    """

    service = MaintenanceService()

    @mcp.tool(
        name="lakehouse_history",
        description=(
            "Retrieve historical health metrics "
            "for an Apache Iceberg table."
        ),
    )
    def lakehouse_history(
        database: str,
        table: str,
    ):
        """
        Returns the historical health metrics
        for the requested table.

        Parameters
        ----------
        database:
            Iceberg database name.

        table:
            orders,
            order_items,
            or both.
        """

        return service.get_table_health_history(
            database=database,
            target=table,
        )