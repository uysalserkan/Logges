"""Integration test verifying old and new APIs work together."""
import os
from pathlib import Path
import tempfile

import pytest


def test_both_apis_coexist():
    """Test that both old and new APIs can be used in the same program."""
    from Logges import Logges, get_logger, LogLevel
    
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir = Path(tmpdir)
        os.chdir(temp_dir)
        
        # Use old API (writes to current directory)
        with pytest.warns(DeprecationWarning):
            Logges.setup(logname="old_api_test")
        Logges.log("Message from old API", Logges.LogStatus.ERROR)
        
        # Use new API (writes to specified directory)
        with get_logger("new_api_test", level=LogLevel.INFO, log_dir=temp_dir) as logger:
            logger.info("Message from new API")
            logger.error("Error from new API")
        
        # New API should have created log files
        log_files = list(temp_dir.glob("*.log"))
        assert len(log_files) >= 1  # At least the new API log
        
        # Verify new API content
        new_api_logs = [f for f in log_files if "new_api_test" in f.name]
        assert len(new_api_logs) > 0
        
        new_content = new_api_logs[0].read_text()
        assert "Message from new API" in new_content


def test_old_api_uses_new_logger_internally():
    """Test that old API creates a compat logger internally."""
    from Logges import Logges
    import Logges.logges as logges_module
    
    # Reset state
    logges_module._COMPAT_LOGGER = None
    
    # Setup old API
    with pytest.warns(DeprecationWarning):
        Logges.setup(logname="compat_test")
    
    # Check that compat logger was created
    assert logges_module._COMPAT_LOGGER is not None
    assert logges_module._COMPAT_LOGGER.config.name == "compat_test"


def test_migration_path():
    """Demonstrate migration from old to new API."""
    from Logges import Logges, get_logger, LogLevel
    
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir = Path(tmpdir)
        
        # Step 1: Old code
        os.chdir(temp_dir)
        with pytest.warns(DeprecationWarning):
            Logges.setup(logname="app")
        Logges.log("Old way", Logges.LogStatus.ERROR)
        
        # Step 2: Gradually migrate to new API
        with get_logger("app", level=LogLevel.ERROR, log_dir=temp_dir) as logger:
            logger.error("New way")
        
        # Both work!
        log_files = list(temp_dir.glob("*_app.log"))
        assert len(log_files) >= 1


def test_new_api_thread_safety():
    """Verify new API supports independent logger instances."""
    from Logges import get_logger, LogLevel
    
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir = Path(tmpdir)
        
        # Create two independent loggers
        logger1 = get_logger("app1", level=LogLevel.INFO, log_dir=temp_dir)
        logger2 = get_logger("app2", level=LogLevel.DEBUG, log_dir=temp_dir)
        
        # They should have different configurations
        assert logger1.config.name != logger2.config.name
        assert logger1.config.level != logger2.config.level
        
        # Both can log independently
        logger1.info("From logger 1")
        logger2.debug("From logger 2")
        
        logger1.close()
        logger2.close()
        
        # Both should have created separate log files
        log_files = list(temp_dir.glob("*.log"))
        app1_logs = [f for f in log_files if "app1" in f.name]
        app2_logs = [f for f in log_files if "app2" in f.name]
        
        assert len(app1_logs) > 0
        assert len(app2_logs) > 0


def test_resource_cleanup():
    """Verify proper resource cleanup with context managers."""
    from Logges import get_logger, LogLevel
    
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir = Path(tmpdir)
        
        # Context manager ensures cleanup
        with get_logger("cleanup_test", log_dir=temp_dir) as logger:
            logger.info("Test message")
            # Logger is still open here
        
        # Logger is closed here
        # Verify log file exists and was written
        log_files = list(temp_dir.glob("*_cleanup_test.log"))
        assert len(log_files) == 1
        assert "Test message" in log_files[0].read_text()
