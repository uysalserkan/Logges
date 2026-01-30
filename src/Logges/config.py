"""Configuration classes for the Logges library.

This module provides dataclasses for configuring loggers and their behavior.
"""

import string
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Optional

from .exceptions import ConfigurationError


class LogLevel(IntEnum):
    """Log severity levels.

    Higher values indicate more severe messages.
    Based on standard logging levels.
    """

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


@dataclass
class LogConfig:
    """Configuration for a Logger instance.

    This dataclass holds all configuration for a logger instance,
    providing sensible defaults and validation.

    Attributes:
        name: Name of the logger (used in log file names)
        level: Minimum log level to record
        log_dir: Directory where log files are stored
        format_string: Format string for log messages
        print_to_console: Whether to print logs to console
        auto_print_level: Auto-print logs at or above this level
        ignored_files: List of file patterns to ignore
        daily_rotation: Whether to create one log file per day
        max_message_size: Maximum size of a single log message in bytes
    """

    name: str
    level: LogLevel = LogLevel.INFO
    log_dir: Path = field(default_factory=Path.cwd)
    format_string: str = "[{time}] [{level:^10}] [{filename}] [{function}]: {message}"
    print_to_console: bool = True
    auto_print_level: LogLevel = LogLevel.ERROR
    ignored_files: list[str] = field(default_factory=list)
    daily_rotation: bool = True
    max_message_size: int = 10_000  # 10KB default

    def __post_init__(self) -> None:
        """Validate and normalize configuration after initialization."""
        # Validate logger name is not empty
        if not self.name:
            raise ConfigurationError("Logger name cannot be empty")

        # Sanitize name to prevent path traversal attacks
        safe_chars = set(string.ascii_letters + string.digits + "-_")
        if not all(c in safe_chars for c in self.name):
            raise ConfigurationError(
                f"Logger name '{self.name}' contains invalid characters. "
                f"Only alphanumeric characters, hyphens, and underscores are allowed."
            )

        # Validate log level
        if not isinstance(self.level, LogLevel):
            raise ConfigurationError(f"Invalid log level: {self.level}")

        # Validate format string is not empty
        if not self.format_string:
            raise ConfigurationError("Format string cannot be empty")

        # Validate max message size
        if self.max_message_size <= 0:
            raise ConfigurationError("max_message_size must be positive")

        # Convert log_dir to Path if it's a string
        if isinstance(self.log_dir, str):
            self.log_dir = Path(self.log_dir)

        # Create log directory if it doesn't exist
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            raise ConfigurationError(f"Cannot create log directory {self.log_dir}: {e}") from e

        # Normalize ignored files to lowercase
        self.ignored_files = [f.lower() for f in self.ignored_files]

    def should_ignore_file(self, filepath: str) -> bool:
        """Check if a file should be ignored based on configuration.

        Args:
            filepath: Path to check against ignored patterns

        Returns:
            True if the file should be ignored, False otherwise
        """
        filepath_lower = filepath.lower()
        return any(pattern in filepath_lower for pattern in self.ignored_files)


@dataclass
class LogRecord:
    """Represents a single log entry.

    This immutable record contains all information about a log message,
    including metadata and the message itself.

    Attributes:
        timestamp: Time when the log was created (HH:MM:SS format)
        level: Severity level of the log
        message: The log message content
        filename: Name of the file where log was called
        function: Name of the function where log was called
        line_number: Line number where log was called
        extra: Additional metadata as key-value pairs
    """

    timestamp: str
    level: LogLevel
    message: str
    filename: str
    function: str
    line_number: int
    extra: dict[str, str] = field(default_factory=dict)

    def format(self, format_string: str) -> str:
        """Format the log record using the provided format string.

        Args:
            format_string: Format string with placeholders

        Returns:
            Formatted log message
        """
        return format_string.format(
            time=self.timestamp,
            level=self.level.name,
            filename=self.filename,
            function=f"{self.function}:{self.line_number}",
            message=self.message,
            **self.extra,
        )
