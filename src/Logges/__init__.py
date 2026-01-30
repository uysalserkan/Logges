"""Logges - An ultimate logging tool for Python.

This package provides both a modern, instance-based logging API and a
backward-compatible static API.

Modern API (Recommended):
    >>> from Logges import get_logger, LogLevel
    >>> logger = get_logger("myapp")
    >>> logger.info("Application started")
    >>> logger.error("An error occurred")

Legacy API (Deprecated):
    >>> from Logges import Logges
    >>> Logges.setup(logname="myapp")
    >>> Logges.log("message", Logges.LogStatus.ERROR)

For new projects, please use the modern Logger API which provides:
- Instance-based design (no global state)
- Thread-safe operation
- Proper resource management
- Type hints throughout
- Pluggable handlers
"""

# Modern API (recommended)
from .logger import Logger, get_logger
from .config import LogConfig, LogLevel, LogRecord
from .handlers import LogHandler, FileHandler, ConsoleHandler
from .exceptions import (
    LoggesError,
    ConfigurationError,
    LogFileError,
    HandlerError,
    FormatterError,
    ExportError,
    RotationError,
)

# Legacy API (deprecated but maintained for compatibility)
from .logges import Logges

__version__ = "2.4"

__all__ = [
    # Modern API
    "Logger",
    "get_logger",
    "LogConfig",
    "LogLevel",
    "LogRecord",
    "LogHandler",
    "FileHandler",
    "ConsoleHandler",
    # Exceptions
    "LoggesError",
    "ConfigurationError",
    "LogFileError",
    "HandlerError",
    "FormatterError",
    "ExportError",
    "RotationError",
    # Legacy API
    "Logges",
]
