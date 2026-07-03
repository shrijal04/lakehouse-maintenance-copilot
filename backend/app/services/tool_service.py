from app.tools.tool_registry import ToolRegistry


class ToolService:
    """
    Determines whether a user's question requires
    backend tools or can be answered directly
    by the LLM.

    Responsibilities:
    - Decide if a tool should be used.
    - Detect which tool to execute.
    - Detect the target table.
    - Detect the target database.
    - Execute the appropriate tool.
    """

    def __init__(self):

        # -----------------------------------------
        # Tool Registry
        # -----------------------------------------

        self.registry = ToolRegistry()

        # -----------------------------------------
        # Keywords that indicate live data is needed
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
    # Should use a backend tool?
    # =====================================================

    def should_use_tool(
        self,
        question: str,
    ) -> bool:
        """
        Return True if the user's question
        requires live backend data.
        """

        question = question.lower()

        return any(
            keyword in question
            for keyword in self.tool_keywords
        )

    # =====================================================
    # Detect Tool
    # =====================================================

    def detect_tool(
        self,
        question: str,
    ) -> str:
        """
        Determine which backend tool should
        handle the user's request.
        """

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
    # Detect Table
    # =====================================================

    def detect_table(
        self,
        question: str,
    ) -> str:
        """
        Determine which Iceberg table
        the user is referring to.
        """

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
    # Detect Database
    # =====================================================

    def detect_database(
        self,
        question: str,
    ) -> str:
        """
        Determine which database/catalog
        should be queried.

        Currently always returns the default
        lakehouse database.
        """

        return "lakehouse"

    # =====================================================
    # Execute Tool
    # =====================================================

    def execute_tool(
        self,
        question: str,
    ):
        """
        Execute the detected backend tool.
        """

        tool_name = self.detect_tool(question)

        database = self.detect_database(question)

        table = self.detect_table(question)

        tool_instance = self.registry.get_tool(
            tool_name
        )

        if tool_instance is None:
            return None

        return tool_instance.execute(
            database=database,
            table=table,
        )