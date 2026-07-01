import uuid


class ConfirmationManager:
    def __init__(self):
        self.pending_confirmations = {}

    def create_confirmation(self):
        """
        Generate a new confirmation ID and store it.
        """
        confirmation_id = str(uuid.uuid4())
        self.pending_confirmations[confirmation_id] = True
        return confirmation_id

    def is_valid_confirmation(self, confirmation_id: str):
        """
        Check whether the confirmation ID is valid.
        """
        return self.pending_confirmations.get(
            confirmation_id,
            False,
        )

    def remove_confirmation(self, confirmation_id: str):
        """
        Remove a confirmation after it has been used.
        """
        self.pending_confirmations.pop(
            confirmation_id,
            None,
        )


# Singleton instance
confirmation_manager = ConfirmationManager()