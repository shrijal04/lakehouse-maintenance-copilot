from fastmcp import FastMCP

from app.tools.health_tool import HealthTool
from app.tools.issues_tool import IssuesTool
from app.tools.maintenance_tool import MaintenanceTool


mcp = FastMCP(
    name="Lakehouse Maintenance MCP"
)


@mcp.tool()
def lakehouse_health(
    database: str,
    table: str,
):
    tool = HealthTool()

    return tool.execute(
        database=database,
        table=table,
    )


@mcp.tool()
def lakehouse_issues(
    database: str,
    table: str,
):
    tool = IssuesTool()

    return tool.execute(
        database=database,
        table=table,
    )


@mcp.tool()
def run_maintenance(
    database: str,
    table: str,
):
    tool = MaintenanceTool()

    return tool.execute(
        database=database,
        table=table,
    )


if __name__ == "__main__":
    mcp.run()