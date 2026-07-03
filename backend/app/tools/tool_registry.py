from app.tools.health_tool import HealthTool
from app.tools.history_tool import HistoryTool
from app.tools.issues_tool import IssuesTool
from app.tools.maintenance_tool import MaintenanceTool


class ToolRegistry:

    def __init__(self):

        self.tools = {
            "health": HealthTool(),
            "issues": IssuesTool(),
            "history": HistoryTool(),
            "maintenance": MaintenanceTool(),
        }

    def get_tool(
        self,
        tool_name: str,
    ):
        return self.tools.get(tool_name)