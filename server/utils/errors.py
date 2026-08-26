class ResearchSourceError(Exception):
    """
    Raised when an external healthcare research
    source cannot be reached or returns an error.
    """

    def __init__(
        self,
        source: str,
        message: str,
    ):
        self.source = source
        self.message = message

        super().__init__(
            f"{source}: {message}"
        )
