class ErrorExplainer:
    """
    Converts technical exceptions into
    user-friendly error messages.
    """

    def explain(
        self,
        error: Exception,
    ):

        text = str(error)

        # ----------------------------------------
        # Iceberg Optimistic Concurrency Conflict
        # ----------------------------------------

        if (
            "ValidationException" in text
            or "Found conflicting files" in text
            or "conflicting files" in text.lower()
        ):

            return {
                "type": "optimistic_concurrency",
                "message": (
                    "Two users tried to modify the same Iceberg table at the same time. "
                    "Apache Iceberg automatically stopped one operation to prevent "
                    "data corruption. No data was lost. You can safely retry the operation."
                ),
            }

        # ----------------------------------------
        # Unknown error
        # ----------------------------------------

        return {
            "type": "unknown",
            "message": text,
        }