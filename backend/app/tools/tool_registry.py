from app.tools.base_tool import BaseTool
from app.tools.health_tool import HealthTool
from app.tools.history_tool import HistoryTool
from app.tools.issues_tool import IssuesTool
from app.tools.maintenance_tool import MaintenanceTool


class ToolRegistry:
    """
    Central registry for all backend tools.

    Adding a new tool only requires:
    1. Creating the tool class.
    2. Registering it here.
    """

    def __init__(self):

        self.tools: dict[str, BaseTool] = {
            "health": HealthTool(),
            "issues": IssuesTool(),
            "history": HistoryTool(),
            "maintenance": MaintenanceTool(),
        }

    def get_tool(
        self,
        tool_name: str,
    ) -> BaseTool | None:

        return self.tools.get(tool_name)