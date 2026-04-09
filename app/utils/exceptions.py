"""Custom exceptions used across the digital library backend."""


class LibraryError(Exception):
    """Base exception for library-related errors."""


class ValidationError(LibraryError):
    """Raised when user input is invalid."""


class EmptyLibraryError(LibraryError):
    """Raised when an operation requires at least one book."""


class BookNotFoundError(LibraryError):
    """Raised when a requested book cannot be found."""


class NavigationError(LibraryError):
    """Raised when navigation cannot move in the requested direction."""
