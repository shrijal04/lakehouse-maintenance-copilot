from app.tools.tool_registry import ToolRegistry


class ToolService:
    """
    Decides whether the AI should use
    backend tools or answer directly
    using the LLM.
    """

    def __init__(self):

        # -----------------------------------------
        # Tool Registry
        # -----------------------------------------

        self.registry = ToolRegistry()

        # -----------------------------------------
        # Keywords that require live data
        # -----------------------------------------

        self.tool_keywords = [

            # Health
            "health",
            "score",
            "snapshot",
            "snapshots",
            "manifest",
            "orphan",
            "file count",
            "files",
            "storage",
            "size",
            "average file",
            "metadata",

            # Maintenance
            "maintenance",
            "compact",
            "compaction",
            "rewrite",
            "optimize",
            "expire",
            "cleanup",
            "clean",
            "vacuum",

            # Dashboard
            "dashboard",
            "issue",
            "issues",
            "warning",
            "critical",

            # History
            "history",
            "trend",

            # Tables
            "orders",
            "order",
            "orders table",
            "order items",
            "order item",
            "order_items",
            "table",

            # Actions
            "run maintenance",
            "execute maintenance",
            "check",
            "show",
            "display",
            "list",

            # Statistics
            "how many",
            "count",
            "latest",
            "current",
        ]

    # =====================================================
    # Should use a tool?
    # =====================================================

    def should_use_tool(
        self,
        question: str,
    ) -> bool:

        question = question.lower()

        return any(
            keyword in question
            for keyword in self.tool_keywords
        )

    # =====================================================
    # Detect which tool
    # =====================================================

    def detect_tool(
        self,
        question: str,
    ) -> str:

        q = question.lower()

        if any(word in q for word in [
            "health",
            "snapshot",
            "manifest",
            "orphan",
            "storage",
            "size",
            "metadata",
        ]):
            return "health"

        if any(word in q for word in [
            "issue",
            "issues",
            "warning",
            "critical",
            "problem",
        ]):
            return "issues"

        if any(word in q for word in [
            "history",
            "trend",
        ]):
            return "history"

        if any(word in q for word in [
            "maintenance",
            "compact",
            "rewrite",
            "expire",
            "cleanup",
            "vacuum",
            "optimize",
        ]):
            return "maintenance"

        return "llm"

    # =====================================================
    # Detect table
    # =====================================================

    def detect_table(
        self,
        question: str,
    ) -> str:

        q = question.lower()

        if any(word in q for word in [
            "order items",
            "order item",
            "order_items",
        ]):
            return "order_items"

        if any(word in q for word in [
            "orders",
            "order",
            "orders table",
        ]):
            return "orders"

        return "both"

    # =====================================================
    # Detect database
    # =====================================================

    def detect_database(
        self,
        question: str,
    ) -> str:

        # Future:
        # Detect the correct catalog/database
        return "lakehouse"

    # =====================================================
    # Execute Tool
    # =====================================================

    def execute_tool(
        self,
        question: str,
    ):

        tool_name = self.detect_tool(question)

        database = self.detect_database(question)

        table = self.detect_table(question)

        tool = self.registry.get_tool(tool_name)

        if tool is None:
            return None

        return tool.execute(
            database=database,
            table=table,
        )