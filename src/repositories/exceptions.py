"""
Repository exceptions.
"""

class RepositoryError(Exception):
    """
    Base class for all repository exceptions.
    """

class DuplicateEmailError(RepositoryError):
    """
    Raised when attempting to insert an email that already exists
    """

class EmailInsertError(RepositoryError):
    """
    Raised when an email cannot be inserted.
    """