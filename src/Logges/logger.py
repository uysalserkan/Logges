"""Modern instance-based Logger class for the Logges library.

This module provides the new, improved Logger class that replaces the static
methods of the old Logges class with proper instance-based design.
"""

import datetime
import sys
from pathlib import Path
from types import FrameType
from typing import Any, Optional

from .config import LogConfig, LogLevel, LogRecord
from .exceptions import ConfigurationError, HandlerError
from .handlers import ConsoleHandler, FileHandler, LogHandler


class Logger:
    """Modern instance-based logger with proper resource management.

    This logger replaces the old static Logges class with a proper
    object-oriented design that supports:
    - Multiple logger instances
    - Thread-safe operation (each instance is independent)
    - Proper resource management via context managers
    - Pluggable handlers for flexible output
    - Type hints throughout

    Example:
        >>> config = LogConfig(name="myapp", level=LogLevel.INFO)
        >>> logger = Logger(config)
        >>> logger.info("Application started")
        >>> logger.error("An error occurred")
        >>> logger.close()

        Or use as context manager:
        >>> with Logger(config) as logger:
        ...     logger.info("Application started")
    """

    def __init__(self, config: LogConfig, handlers: Optional[list[LogHandler]] = None) -> None:
        """Initialize a new Logger instance.

        Args:
            config: Configuration for this logger
            handlers: Optional list of handlers. If None, creates default file+console handlers

        Raises:
            ConfigurationError: If configuration is invalid
        """
        self.config = config

        # Set up handlers
        if handlers is not None:
            self.handlers = handlers
        else:
            # Create default handlers
            self.handlers = self._create_default_handlers()

    def _create_default_handlers(self) -> list[LogHandler]:
        """Create default file and console handlers.

        Returns:
            List containing a file handler and optional console handler
        """
        handlers: list[LogHandler] = []

        # File handler - always enabled
        log_file = self._get_log_filepath()
        try:
            file_handler = FileHandler(log_file)
            handlers.append(file_handler)
        except Exception as e:
            # If we can't create file handler, warn but continue with console only
            print(f"Warning: Could not create file handler: {e}", file=sys.stderr)

        # Console handler - if enabled in config
        if self.config.print_to_console:
            console_handler = ConsoleHandler(use_stderr_for_errors=True)
            handlers.append(console_handler)

        return handlers

    def _get_log_filepath(self) -> Path:
        """Get the path for the log file based on configuration.

        Returns:
            Path to the log file
        """
        if self.config.daily_rotation:
            # Include date in filename
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = f"{date_str}_{self.config.name}.log"
        else:
            filename = f"{self.config.name}.log"

        return self.config.log_dir / filename

    def _get_caller_info(self, depth: int = 3) -> tuple[str, str, int]:
        """Get information about the caller of the log method.

        Uses frame introspection to determine the file, function, and line number
        where the log method was called. Tries multiple depths if the specified
        depth fails.

        Args:
            depth: Stack depth to check (default: 3)

        Returns:
            Tuple of (filepath, function_name, line_number)
        """
        try:
            # Try the specified depth first
            frame: Optional[FrameType] = sys._getframe(depth)
            if frame is None:
                return ("unknown", "unknown", 0)

            filepath = frame.f_code.co_filename
            function_name = frame.f_code.co_name
            line_number = frame.f_lineno

            # Extract just the filename from the full path
            filename = Path(filepath).name

            return (filename, function_name, line_number)
        except (ValueError, AttributeError):
            # If specified depth fails, try to find the right frame
            # by looking for a frame that's not in logger.py
            try:
                for d in range(2, 7):
                    try:
                        frame = sys._getframe(d)
                        if frame and "logger.py" not in frame.f_code.co_filename:
                            filepath = frame.f_code.co_filename
                            function_name = frame.f_code.co_name
                            line_number = frame.f_lineno
                            filename = Path(filepath).name
                            return (filename, function_name, line_number)
                    except ValueError:
                        continue
            except Exception:
                pass

            # If all else fails, return unknowns
            return ("unknown", "unknown", 0)

    def _should_log(self, level: LogLevel, filepath: str) -> bool:
        """Determine if a log message should be recorded.

        Args:
            level: Log level of the message
            filepath: File path where log was called

        Returns:
            True if the message should be logged, False otherwise
        """
        # Check level filtering
        if level < self.config.level:
            return False

        # Check if file is ignored
        if self.config.should_ignore_file(filepath):
            return False

        return True

    def log(self, message: str | Any, level: LogLevel, **extra: str) -> None:
        """Log a message at the specified level.

        This is the core logging method. Most users will use the convenience
        methods (debug, info, warning, error, critical) instead.

        Args:
            message: The message to log (will be converted to string if needed)
            level: Severity level of the message
            **extra: Additional key-value pairs to include in the log
        """
        # Convert message to string if needed
        if not isinstance(message, str):
            message = str(message)

        # Truncate message if it exceeds max size
        if len(message) > self.config.max_message_size:
            truncated_suffix = f"... (truncated from {len(message)} bytes)"
            max_content = self.config.max_message_size - len(truncated_suffix)
            message = message[:max_content] + truncated_suffix

        # Get caller information
        filename, function_name, line_number = self._get_caller_info()

        # Check if we should log this
        if not self._should_log(level, filename):
            return

        # Get current time
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        # Create log record
        record = LogRecord(
            timestamp=timestamp,
            level=level,
            message=message,
            filename=filename,
            function=function_name,
            line_number=line_number,
            extra=extra,
        )

        # Early return if no handlers
        if not self.handlers:
            return

        # Format the message
        formatted_message = record.format(self.config.format_string)

        # Emit to all handlers
        for handler in self.handlers:
            try:
                handler.emit(record, formatted_message)
            except HandlerError as e:
                # Log handler errors to stderr, but don't crash
                print(f"Handler error: {e}", file=sys.stderr)

    # Convenience methods for each log level

    def debug(self, message: str | Any, **extra: str) -> None:
        """Log a DEBUG level message.

        Args:
            message: The message to log
            **extra: Additional metadata
        """
        self.log(message, LogLevel.DEBUG, **extra)

    def info(self, message: str | Any, **extra: str) -> None:
        """Log an INFO level message.

        Args:
            message: The message to log
            **extra: Additional metadata
        """
        self.log(message, LogLevel.INFO, **extra)

    def warning(self, message: str | Any, **extra: str) -> None:
        """Log a WARNING level message.

        Args:
            message: The message to log
            **extra: Additional metadata
        """
        self.log(message, LogLevel.WARNING, **extra)

    def error(self, message: str | Any, **extra: str) -> None:
        """Log an ERROR level message.

        Args:
            message: The message to log
            **extra: Additional metadata
        """
        self.log(message, LogLevel.ERROR, **extra)

    def critical(self, message: str | Any, **extra: str) -> None:
        """Log a CRITICAL level message.

        Args:
            message: The message to log
            **extra: Additional metadata
        """
        self.log(message, LogLevel.CRITICAL, **extra)

    def close(self) -> None:
        """Close all handlers and release resources.

        This should be called when the logger is no longer needed.
        """
        for handler in self.handlers:
            try:
                handler.close()
            except Exception as e:
                print(f"Error closing handler: {e}", file=sys.stderr)

    # Context manager support

    def __enter__(self) -> "Logger":
        """Support context manager protocol."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore[no-untyped-def]
        """Ensure cleanup when used as context manager."""
        self.close()


def get_logger(
    name: str, level: LogLevel = LogLevel.INFO, log_dir: Optional[Path] = None
) -> Logger:
    """Convenience function to create a logger with sensible defaults.

    This function provides a simple API for creating loggers without
    needing to manually construct LogConfig objects.

    Args:
        name: Name of the logger
        level: Minimum log level (default: INFO)
        log_dir: Directory for log files (default: current directory)

    Returns:
        Configured Logger instance

    Example:
        >>> logger = get_logger("myapp")
        >>> logger.info("Hello, world!")
        >>> logger.close()
    """
    if log_dir is None:
        log_dir = Path.cwd()

    config = LogConfig(name=name, level=level, log_dir=log_dir)

    return Logger(config)
