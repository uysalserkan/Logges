"""Custom exceptions for the Logges library.

This module defines all custom exceptions used throughout the Logges library,
providing clear error types for different failure modes.
"""


class LoggesError(Exception):
    """Base exception for all Logges-related errors.

    All custom exceptions in the Logges library should inherit from this base class.
    This allows users to catch all Logges-specific errors with a single except clause.
    """


class ConfigurationError(LoggesError):
    """Raised when there's an error in logger configuration.

    Examples:
        - Invalid log level specified
        - Invalid file path provided
        - Missing required configuration parameters
    """


class LogFileError(LoggesError):
    """Raised when log file operations fail.

    Examples:
        - Cannot open log file for writing
        - Disk full errors
        - Permission denied errors
        - File system errors
    """


class HandlerError(LoggesError):
    """Raised when a log handler encounters an error.

    Examples:
        - Handler initialization failure
        - Handler emit() failure
        - Handler cleanup failure
    """


class FormatterError(LoggesError):
    """Raised when log formatting fails.

    Examples:
        - Invalid format string
        - Missing required fields in format
        - Type conversion errors during formatting
    """


class ExportError(LoggesError):
    """Raised when log export operations fail.

    Examples:
        - PDF generation failure
        - Markdown export failure
        - Missing dependencies for export
    """


class RotationError(LoggesError):
    """Raised when log rotation fails.

    Examples:
        - Cannot rename rotated file
        - Cannot delete old log files
        - Rotation policy violation
    """
