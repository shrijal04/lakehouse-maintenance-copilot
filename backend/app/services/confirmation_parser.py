class ConfirmationParser:
    """
    Detect whether the user's response
    confirms or rejects an action.
    """

    YES_WORDS = {
        "yes",
        "y",
        "yeah",
        "yep",
        "sure",
        "ok",
        "okay",
        "confirm",
        "continue",
        "proceed",
        "go ahead",
        "run it",
        "do it",
        "please continue",
    }

    NO_WORDS = {
        "no",
        "n",
        "cancel",
        "stop",
        "abort",
        "don't",
        "do not",
        "never mind",
        "no thanks",
    }

    def is_confirmation(self, text: str) -> bool:

        text = text.lower().strip()

        return any(
            word in text
            for word in self.YES_WORDS
        )

    def is_rejection(self, text: str) -> bool:

        text = text.lower().strip()

        return any(
            word in text
            for word in self.NO_WORDS
        )