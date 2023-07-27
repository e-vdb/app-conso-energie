"""Exceptions for the app."""


class WorksheetError(Exception):
    """Base class for exceptions in this module."""


class NoIndexRecordedYet(WorksheetError):
    """Exception raised when no index is recorded yet."""

    def __init__(self):
        """Initialize the class."""
        self.message = "No index recorded yet."
        super().__init__(self.message)
