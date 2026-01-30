"""Pytest configuration and fixtures for Logges tests."""
import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for each test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_log_file(temp_dir: Path) -> Path:
    """Provide a temporary log file path."""
    return temp_dir / "test.log"


@pytest.fixture
def sample_log_content() -> str:
    """Provide sample log content for testing."""
    return """[12:34:56] [  DEBUG   ] [test.py] [test_func:10]: Debug message
[12:34:57] [   INFO   ] [test.py] [test_func:11]: Info message
[12:34:58] [ WARNING  ] [test.py] [test_func:12]: Warning message
[12:34:59] [  ERROR   ] [test.py] [test_func:13]: Error message
[12:35:00] [ CRITICAL ] [test.py] [test_func:14]: Critical message
"""


@pytest.fixture
def sample_log_file(temp_dir: Path, sample_log_content: str) -> Path:
    """Create a sample log file for testing."""
    log_file = temp_dir / "2026-01-30_test.log"
    log_file.write_text(sample_log_content)
    return log_file


@pytest.fixture(autouse=True)
def reset_logges_state():
    """Reset Logges global state before each test."""
    import Logges.logges as logges_module
    
    # Reset globals
    logges_module.FILENAME = None
    logges_module.SAVINGPATH = None
    logges_module.STATUS_LEVEL = None
    logges_module.IGNORE_FILES_AND_DIRS = []
    
    # Clean environment
    if "print_status" in os.environ:
        del os.environ["print_status"]
    
    yield
    
    # Cleanup after test
    logges_module.FILENAME = None
    logges_module.SAVINGPATH = None
    logges_module.STATUS_LEVEL = None
    logges_module.IGNORE_FILES_AND_DIRS = []
    
    if "print_status" in os.environ:
        del os.environ["print_status"]
