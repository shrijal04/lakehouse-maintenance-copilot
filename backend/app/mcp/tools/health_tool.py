from fastmcp import FastMCP

from app.services.maintenance_service import (
    MaintenanceService,
)


def register_health_tool(
    mcp: FastMCP,
):
    """
    Register the Lakehouse Health Tool
    with the MCP server.
    """

    service = MaintenanceService()

    @mcp.tool(
        name="lakehouse_health",
        description=(
            "Get the current health metrics "
            "for an Apache Iceberg table."
        ),
    )
    def lakehouse_health(
        database: str,
        table: str,
    ):
        """
        Returns live health metrics
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

        return service.get_table_health(
            database=database,
            target=table,
        )