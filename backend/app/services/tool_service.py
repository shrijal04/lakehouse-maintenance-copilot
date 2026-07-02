class ToolService:
    """
    Decides whether the AI should use
    the LLM only or execute backend tools.

    Later this class will call Spark,
    Iceberg and Maintenance APIs.
    """

    def __init__(self):
        # Questions that need live data
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

    def should_use_tool(self, question: str) -> bool:
        """
        Returns True if the question should
        use backend tools instead of only
        sending it to the LLM.
        """

        question = question.lower()

        return any(
            keyword in question
            for keyword in self.tool_keywords
        )

    def detect_tool(self, question: str) -> str:
        """
        Decide which backend tool should run.
        """

        q = question.lower()

        # -------------------------
        # Health
        # -------------------------

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

        # -------------------------
        # Issues
        # -------------------------

        if any(word in q for word in [
            "issue",
            "warning",
            "critical",
            "problem",
        ]):
            return "issues"

        # -------------------------
        # History
        # -------------------------

        if any(word in q for word in [
            "history",
            "trend",
        ]):
            return "history"

        # -------------------------
        # Maintenance
        # -------------------------

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

    def detect_table(self, question: str) -> str:
        """
        Determine which table the user
        is referring to.
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

    def detect_database(self, question: str) -> str:
        """
        Future support for multiple databases.

        For now always use lakehouse.
        """

        return "lakehouse"

    def execute_tool(self, question: str):
        """
        Placeholder.

        Later this will call the appropriate
        backend service (Health, Issues,
        History, Maintenance, etc.).
        """

        tool = self.detect_tool(question)
        table = self.detect_table(question)
        database = self.detect_database(question)

        print(
            f"Tool={tool}, "
            f"Database={database}, "
            f"Table={table}"
        )

        # Will later call backend services.
        return None