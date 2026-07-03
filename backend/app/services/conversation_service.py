class ConversationService:
    """
    Stores temporary conversation state.

    Currently this is only used to keep
    track of pending maintenance requests.

    Later this can be replaced by Redis,
    a database, or a proper session store.
    """

    def __init__(self):

        self.pending_actions = {}

    # -------------------------------------------------
    # Store Pending Action
    # -------------------------------------------------

    def set_pending_action(
        self,
        session_id: str,
        action: dict,
    ):

        self.pending_actions[session_id] = action

    # -------------------------------------------------
    # Get Pending Action
    # -------------------------------------------------

    def get_pending_action(
        self,
        session_id: str,
    ):

        return self.pending_actions.get(session_id)

    # -------------------------------------------------
    # Clear Pending Action
    # -------------------------------------------------

    def clear_pending_action(
        self,
        session_id: str,
    ):

        self.pending_actions.pop(
            session_id,
            None,
        )


# -------------------------------------------------
# Singleton
# -------------------------------------------------

conversation_service = ConversationService()