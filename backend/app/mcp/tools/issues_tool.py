from fastmcp import FastMCP

from app.services.maintenance_service import (
    MaintenanceService,
)


def register_issues_tool(
    mcp: FastMCP,
):
    """
    Register the Lakehouse Issues Tool
    with the MCP server.
    """

    service = MaintenanceService()

    @mcp.tool(
        name="lakehouse_issues",
        description=(
            "Get the current health issues "
            "for an Apache Iceberg table."
        ),
    )
    def lakehouse_issues(
        database: str,
        table: str,
    ):
        """
        Returns the detected issues for
        the requested table.

        Parameters
        ----------
        database:
            Iceberg database name.

        table:
            orders,
            order_items,
            or both.
        """

        return service.get_table_issues(
            database=database,
            target=table,
        )