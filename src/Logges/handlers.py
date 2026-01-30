"""Handler classes for the Logges library.

This module provides the handler pattern for flexible log output destinations.
Handlers can write to files, console, or other destinations.
"""

import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, TextIO

from .config import LogRecord
from .exceptions import HandlerError, LogFileError


class LogHandler(ABC):
    """Abstract base class for all log handlers.

    Handlers are responsible for writing log records to a destination
    (file, console, network, etc.). Each handler manages its own resources
    and provides proper cleanup.
    """

    @abstractmethod
    def emit(self, record: LogRecord, formatted_message: str) -> None:
        """Write a log record to the handler's destination.

        Args:
            record: The log record to write
            formatted_message: Pre-formatted log message string

        Raises:
            HandlerError: If the handler cannot write the log
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Clean up handler resources.

        This method should be called when the handler is no longer needed.
        It should release any held resources (files, connections, etc.).
        """
        pass

    def __enter__(self) -> "LogHandler":
        """Support context manager protocol."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore[no-untyped-def]
        """Ensure cleanup when used as context manager."""
        self.close()


class FileHandler(LogHandler):
    """Handler that writes logs to a file with proper resource management.

    This handler opens a file for appending and writes log records to it.
    It uses context managers to ensure proper file closure even in error cases.

    Attributes:
        filepath: Path to the log file
        _fallback_file: Fallback file for critical errors
        _stderr_failed: Flag to track if stderr writing failed
    """

    def __init__(self, filepath: Path) -> None:
        """Initialize file handler.

        Args:
            filepath: Path where logs should be written

        Raises:
            LogFileError: If the file cannot be opened for writing
        """
        self.filepath = filepath
        self._stderr_failed = False
        self._fallback_file = Path("/tmp/logges_errors.log")

        # Ensure parent directory exists
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

        # Test that we can write to the file
        try:
            with open(self.filepath, "a") as f:
                pass  # Just test we can open it
        except (IOError, OSError) as e:
            raise LogFileError(f"Cannot write to log file {filepath}: {e}") from e

    def emit(self, record: LogRecord, formatted_message: str) -> None:
        """Write a log record to the file.

        Args:
            record: The log record to write
            formatted_message: Pre-formatted log message

        Raises:
            HandlerError: If writing to the file fails
        """
        try:
            with open(self.filepath, "a") as f:
                f.write(formatted_message + "\n")
        except (IOError, OSError) as e:
            # Don't let logging errors crash the application
            # Try to write to stderr as fallback
            try:
                print(f"Logging error: {e}", file=sys.stderr)
                print(f"Failed to log: {formatted_message}", file=sys.stderr)
            except Exception:
                # Last resort: try to write to a fallback file
                if not self._stderr_failed:
                    self._stderr_failed = True
                    try:
                        with open(self._fallback_file, "a") as f:
                            f.write(f"[CRITICAL] Logging system failure: {e}\n")
                            f.write(f"Failed message: {formatted_message}\n")
                    except Exception:
                        pass  # If fallback also fails, give up silently

    def close(self) -> None:
        """Close the file handler.

        Note: This handler uses context managers internally,
        so there's no persistent file handle to close.
        """
        pass  # Nothing to close since we use context managers


class ConsoleHandler(LogHandler):
    """Handler that writes logs to console (stdout/stderr).

    This handler writes log records to the console. Error and Critical
    messages go to stderr, all others go to stdout.

    Attributes:
        use_stderr_for_errors: If True, ERROR and CRITICAL go to stderr
    """

    def __init__(self, use_stderr_for_errors: bool = True) -> None:
        """Initialize console handler.

        Args:
            use_stderr_for_errors: Whether to use stderr for error-level logs
        """
        self.use_stderr_for_errors = use_stderr_for_errors

    def emit(self, record: LogRecord, formatted_message: str) -> None:
        """Write a log record to the console.

        Args:
            record: The log record to write
            formatted_message: Pre-formatted log message
        """
        from .config import LogLevel

        # Determine output stream
        if self.use_stderr_for_errors and record.level >= LogLevel.ERROR:
            output = sys.stderr
        else:
            output = sys.stdout

        try:
            print(formatted_message, file=output)
        except Exception as e:
            # If console printing fails, there's not much we can do
            # Try stderr as last resort
            try:
                print(f"Console logging error: {e}", file=sys.stderr)
            except Exception:
                pass  # Give up silently

    def close(self) -> None:
        """Close the console handler.

        Note: We don't close stdout/stderr as they're system streams.
        """
        pass  # Don't close system streams
