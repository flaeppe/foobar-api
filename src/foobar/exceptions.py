class NotCancelableException(Exception):
    """Raised when a purchase cannot be canceled."""


class InvalidTransition(Exception):
    """Raised when an enum is transitioning to an invalid value"""
