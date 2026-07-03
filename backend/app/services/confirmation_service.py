import uuid


class ConfirmationManager:
    """
    Manages pending confirmations for
    maintenance operations.

    For now, confirmations are stored
    in memory. This can later be replaced
    with Redis or a database.
    """

    def __init__(self):
        self.pending_confirmations = {}

    def create_confirmation(
        self,
        database: str,
        table: str,
        action: str,
    ) -> str:
        """
        Create a new confirmation request.

        Returns the generated confirmation ID.
        """

        confirmation_id = str(uuid.uuid4())

        self.pending_confirmations[confirmation_id] = {
            "confirmation_id": confirmation_id,
            "database": database,
            "table": table,
            "action": action,
        }

        return confirmation_id

    def is_valid_confirmation(
        self,
        confirmation_id: str,
    ) -> bool:
        """
        Check whether the confirmation ID exists.
        """

        return confirmation_id in self.pending_confirmations

    def get_confirmation(
        self,
        confirmation_id: str,
    ):
        """
        Retrieve the stored confirmation details.
        """

        return self.pending_confirmations.get(
            confirmation_id
        )

    def remove_confirmation(
        self,
        confirmation_id: str,
    ):
        """
        Remove a confirmation after it has
        been completed or cancelled.
        """

        self.pending_confirmations.pop(
            confirmation_id,
            None,
        )


# ---------------------------------------------------
# Singleton instance
# ---------------------------------------------------

confirmation_manager = ConfirmationManager()