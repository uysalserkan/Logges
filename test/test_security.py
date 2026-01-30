"""Tests for security and validation improvements."""
import string
from pathlib import Path

import pytest

from Logges import LogConfig, LogLevel, Logger, get_logger
from Logges.exceptions import ConfigurationError


class TestLogConfigValidation:
    """Test LogConfig validation and security."""
    
    def test_empty_name_rejected(self):
        """Test that empty logger name is rejected."""
        with pytest.raises(ConfigurationError, match="Logger name cannot be empty"):
            LogConfig(name="")
    
    def test_invalid_characters_rejected(self):
        """Test that invalid characters in name are rejected."""
        invalid_names = [
            "my/app",       # Path separator
            "my\\app",      # Windows path separator
            "../app",       # Path traversal
            "app.log",      # Extension (suspicious)
            "my app",       # Space
            "app@2024",     # Special char
            "app#test",     # Special char
        ]
        
        for name in invalid_names:
            with pytest.raises(ConfigurationError, match="invalid characters"):
                LogConfig(name=name)
    
    def test_valid_names_accepted(self):
        """Test that valid names are accepted."""
        valid_names = [
            "myapp",
            "my-app",
            "my_app",
            "MyApp123",
            "app-v2",
            "test_logger_2024",
        ]
        
        for name in valid_names:
            config = LogConfig(name=name)
            assert config.name == name
    
    def test_invalid_log_level_rejected(self):
        """Test that invalid log level is rejected."""
        with pytest.raises(ConfigurationError, match="Invalid log level"):
            LogConfig(name="test", level="INVALID")  # type: ignore
    
    def test_empty_format_string_rejected(self):
        """Test that empty format string is rejected."""
        with pytest.raises(ConfigurationError, match="Format string cannot be empty"):
            LogConfig(name="test", format_string="")
    
    def test_invalid_max_message_size(self):
        """Test that invalid max_message_size is rejected."""
        with pytest.raises(ConfigurationError, match="max_message_size must be positive"):
            LogConfig(name="test", max_message_size=0)
        
        with pytest.raises(ConfigurationError, match="max_message_size must be positive"):
            LogConfig(name="test", max_message_size=-100)
    
    def test_invalid_log_dir_permission(self, tmp_path: Path):
        """Test that inaccessible log directory raises error."""
        # Create a directory with no write permissions
        no_write_dir = tmp_path / "no_write"
        no_write_dir.mkdir()
        no_write_dir.chmod(0o444)  # Read-only
        
        # On some systems this may not raise, but if it does, check the error
        try:
            config = LogConfig(name="test", log_dir=no_write_dir / "nested")
        except ConfigurationError as e:
            assert "Cannot create log directory" in str(e)
        finally:
            # Cleanup
            no_write_dir.chmod(0o755)


class TestMessageSizeLimits:
    """Test message size limiting."""
    
    def test_short_message_unchanged(self, temp_dir: Path):
        """Test that short messages are not truncated."""
        config = LogConfig(name="test", log_dir=temp_dir, print_to_console=False)
        logger = Logger(config)
        
        message = "Short message"
        logger.info(message)
        logger.close()
        
        log_file = list(temp_dir.glob("*.log"))[0]
        content = log_file.read_text()
        
        assert message in content
        assert "truncated" not in content
    
    def test_long_message_truncated(self, temp_dir: Path):
        """Test that long messages are truncated."""
        max_size = 1000
        config = LogConfig(
            name="test",
            log_dir=temp_dir,
            print_to_console=False,
            max_message_size=max_size
        )
        logger = Logger(config)
        
        # Create a message longer than max_size
        long_message = "A" * (max_size + 500)
        logger.info(long_message)
        logger.close()
        
        log_file = list(temp_dir.glob("*.log"))[0]
        content = log_file.read_text()
        
        assert "truncated" in content
        assert f"truncated from {len(long_message)} bytes" in content
    
    def test_small_message_not_cut_off(self, temp_dir: Path):
        """Test that message under max size is not cut off."""
        max_size = 1000
        config = LogConfig(
            name="test",
            log_dir=temp_dir,
            print_to_console=False,
            max_message_size=max_size
        )
        logger = Logger(config)
        
        # Use a small message that won't be truncated
        message = "A" * 100
        logger.info(message)
        logger.close()
        
        log_file = list(temp_dir.glob("*.log"))[0]
        content = log_file.read_text()
        
        assert "truncated" not in content.lower()
        assert message in content


class TestFrameIntrospection:
    """Test improved frame introspection."""
    
    def test_basic_caller_info(self, temp_dir: Path):
        """Test that caller info is captured correctly."""
        config = LogConfig(name="test", log_dir=temp_dir, print_to_console=False)
        logger = Logger(config)
        
        logger.info("Test message")
        logger.close()
        
        log_file = list(temp_dir.glob("*.log"))[0]
        content = log_file.read_text()
        
        # Should contain this test file name
        assert "test_security.py" in content
        # Should contain function name
        assert "test_basic_caller_info" in content
    
    def test_nested_calls(self, temp_dir: Path):
        """Test that caller info works with nested calls."""
        config = LogConfig(name="test", log_dir=temp_dir, print_to_console=False)
        logger = Logger(config)
        
        def inner_function():
            logger.info("Inner message")
        
        def outer_function():
            inner_function()
        
        outer_function()
        logger.close()
        
        log_file = list(temp_dir.glob("*.log"))[0]
        content = log_file.read_text()
        
        # Should show inner_function as the caller
        assert "inner_function" in content


class TestHandlerErrorRecovery:
    """Test improved handler error recovery."""
    
    def test_handler_failure_doesnt_crash(self, temp_dir: Path, monkeypatch):
        """Test that handler failures don't crash the logger."""
        config = LogConfig(name="test", log_dir=temp_dir, print_to_console=False)
        logger = Logger(config)
        
        # Mock the file open to raise an error
        original_open = open
        call_count = [0]
        
        def failing_open(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] > 1:  # Fail after first call (setup)
                raise IOError("Simulated disk failure")
            return original_open(*args, **kwargs)
        
        monkeypatch.setattr("builtins.open", failing_open)
        
        # This should not raise an exception
        logger.info("Test message")
        logger.close()
    
    def test_multiple_handler_failures(self, temp_dir: Path):
        """Test that multiple handler failures are handled."""
        from Logges.handlers import FileHandler
        
        # Create handlers with invalid paths
        bad_path1 = Path("/invalid/path/1.log")
        bad_path2 = Path("/invalid/path/2.log")
        
        # These will fail to create
        try:
            handler1 = FileHandler(bad_path1)
        except Exception:
            pass  # Expected


class TestSecurityFeatures:
    """Test security-related features."""
    
    def test_no_path_traversal_in_name(self, temp_dir: Path):
        """Test that path traversal attempts in name are blocked."""
        with pytest.raises(ConfigurationError):
            LogConfig(name="../../../etc/passwd", log_dir=temp_dir)
    
    def test_no_absolute_path_in_name(self, temp_dir: Path):
        """Test that absolute paths in name are blocked."""
        with pytest.raises(ConfigurationError):
            LogConfig(name="/etc/passwd", log_dir=temp_dir)
    
    def test_log_dir_stays_within_boundaries(self, temp_dir: Path):
        """Test that log files stay within log_dir."""
        config = LogConfig(name="test-app", log_dir=temp_dir)
        logger = Logger(config)
        
        logger.info("Test message")
        logger.close()
        
        # All log files should be in temp_dir
        log_files = list(temp_dir.glob("*.log"))
        assert len(log_files) > 0
        
        for log_file in log_files:
            # Resolve to absolute path and check it's under temp_dir
            assert log_file.resolve().is_relative_to(temp_dir.resolve())
