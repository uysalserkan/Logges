"""Tests for core Logges functionality."""
import os
from pathlib import Path

import pytest

from Logges import Logges


class TestLoggesSetup:
    """Test Logges.setup() method."""
    
    def test_setup_with_custom_name(self, temp_dir: Path):
        """Test setup with custom log name."""
        os.chdir(temp_dir)
        Logges.setup(logname="custom_log")
        
        import Logges.logges as logges_module
        assert logges_module.FILENAME == "custom_log"
        assert logges_module.SAVINGPATH == str(temp_dir)
        assert logges_module.STATUS_LEVEL == Logges.LogStatus.ERROR.value
    
    def test_setup_with_status_level(self, temp_dir: Path):
        """Test setup with custom status level."""
        os.chdir(temp_dir)
        Logges.setup(
            logname="test_log",
            status_level=Logges.LogStatus.INFO
        )
        
        import Logges.logges as logges_module
        assert logges_module.STATUS_LEVEL == Logges.LogStatus.INFO.value
    
    def test_setup_print_status_true(self, temp_dir: Path):
        """Test setup with print_status=True."""
        os.chdir(temp_dir)
        Logges.setup(logname="test", print_status=True)
        
        assert os.environ.get("print_status") == "True"
    
    def test_setup_print_status_false(self, temp_dir: Path):
        """Test setup with print_status=False."""
        os.chdir(temp_dir)
        Logges.setup(logname="test", print_status=False)
        
        assert os.environ.get("print_status") == "False"


class TestLoggesLog:
    """Test Logges.log() method."""
    
    def test_log_creates_file(self, temp_dir: Path):
        """Test that logging creates a log file."""
        os.chdir(temp_dir)
        Logges.setup(logname="test_log")
        Logges.log("Test message", Logges.LogStatus.INFO)
        
        # Find created log file
        log_files = list(temp_dir.glob("*.log"))
        assert len(log_files) == 1
        assert log_files[0].exists()
    
    def test_log_writes_message(self, temp_dir: Path):
        """Test that log message is written to file."""
        os.chdir(temp_dir)
        Logges.setup(logname="test_log")
        Logges.log("Test message", Logges.LogStatus.ERROR)
        
        log_file = list(temp_dir.glob("*.log"))[0]
        content = log_file.read_text()
        
        assert "Test message" in content
        assert "ERROR" in content
    
    def test_log_multiple_messages(self, temp_dir: Path):
        """Test logging multiple messages."""
        os.chdir(temp_dir)
        Logges.setup(logname="test_log")
        
        messages = ["First message", "Second message", "Third message"]
        for msg in messages:
            Logges.log(msg, Logges.LogStatus.INFO)
        
        log_file = list(temp_dir.glob("*.log"))[0]
        content = log_file.read_text()
        
        for msg in messages:
            assert msg in content
    
    def test_log_different_levels(self, temp_dir: Path):
        """Test logging with different log levels."""
        os.chdir(temp_dir)
        Logges.setup(logname="test_log")
        
        levels = [
            Logges.LogStatus.DEBUG,
            Logges.LogStatus.INFO,
            Logges.LogStatus.WARNING,
            Logges.LogStatus.ERROR,
            Logges.LogStatus.CRITICAL,
        ]
        
        for level in levels:
            Logges.log(f"Message at {level.name}", level)
        
        log_file = list(temp_dir.glob("*.log"))[0]
        content = log_file.read_text()
        
        for level in levels:
            assert level.name in content
    
    def test_log_non_string_message(self, temp_dir: Path):
        """Test logging non-string objects."""
        os.chdir(temp_dir)
        Logges.setup(logname="test_log")
        
        Logges.log(123, Logges.LogStatus.INFO)
        Logges.log([1, 2, 3], Logges.LogStatus.INFO)
        Logges.log({"key": "value"}, Logges.LogStatus.INFO)
        
        log_file = list(temp_dir.glob("*.log"))[0]
        content = log_file.read_text()
        
        assert "123" in content
        assert "[1, 2, 3]" in content
        assert "{'key': 'value'}" in content


class TestLoggesIgnoreFiles:
    """Test Logges.ignore_files() method."""
    
    def test_ignore_single_file(self, temp_dir: Path):
        """Test ignoring a single file."""
        Logges.ignore_files("test_file.py")
        
        import Logges.logges as logges_module
        assert "test_file.py" in logges_module.IGNORE_FILES_AND_DIRS
    
    def test_ignore_multiple_files(self, temp_dir: Path):
        """Test ignoring multiple files."""
        files = ["file1.py", "file2.py", "file3.py"]
        Logges.ignore_files(files)
        
        import Logges.logges as logges_module
        for file in files:
            assert file in logges_module.IGNORE_FILES_AND_DIRS
    
    def test_ignore_files_case_insensitive(self, temp_dir: Path):
        """Test that ignore is case-insensitive."""
        Logges.ignore_files("TEST_FILE.PY")
        
        import Logges.logges as logges_module
        assert "test_file.py" in logges_module.IGNORE_FILES_AND_DIRS


class TestLoggesInLog:
    """Test Logges.in_log() method."""
    
    def test_in_log_single_keyword_found(self, temp_dir: Path, sample_log_file: Path):
        """Test searching for a single keyword that exists."""
        os.chdir(temp_dir)
        import Logges.logges as logges_module
        logges_module.FILENAME = "test"
        logges_module.SAVINGPATH = str(temp_dir)
        
        result = Logges.in_log("Debug message")
        assert result is True
    
    def test_in_log_single_keyword_not_found(self, temp_dir: Path, sample_log_file: Path):
        """Test searching for a keyword that doesn't exist."""
        os.chdir(temp_dir)
        import Logges.logges as logges_module
        logges_module.FILENAME = "test"
        logges_module.SAVINGPATH = str(temp_dir)
        
        result = Logges.in_log("NonexistentKeyword")
        assert result is False
    
    def test_in_log_multiple_keywords_all_found(self, temp_dir: Path, sample_log_file: Path):
        """Test searching for multiple keywords that all exist."""
        os.chdir(temp_dir)
        import Logges.logges as logges_module
        logges_module.FILENAME = "test"
        logges_module.SAVINGPATH = str(temp_dir)
        
        result = Logges.in_log(["Debug", "message"])
        assert result is True


class TestLogStatus:
    """Test LogStatus enum."""
    
    def test_log_status_values(self):
        """Test that LogStatus has correct values."""
        assert Logges.LogStatus.DEBUG.value == 0
        assert Logges.LogStatus.INFO.value == 1
        assert Logges.LogStatus.WARNING.value == 2
        assert Logges.LogStatus.ERROR.value == 3
        assert Logges.LogStatus.CRITICAL.value == 4
    
    def test_log_status_names(self):
        """Test that LogStatus has correct names."""
        assert Logges.LogStatus.DEBUG.name == "DEBUG"
        assert Logges.LogStatus.INFO.name == "INFO"
        assert Logges.LogStatus.WARNING.name == "WARNING"
        assert Logges.LogStatus.ERROR.name == "ERROR"
        assert Logges.LogStatus.CRITICAL.name == "CRITICAL"
    
    def test_get_blank_dict(self):
        """Test get_blank_dict returns correct structure."""
        result = Logges.LogStatus.get_blank_dict()
        
        assert isinstance(result, dict)
        assert result["DEBUG"] == 0
        assert result["INFO"] == 0
        assert result["WARNING"] == 0
        assert result["ERROR"] == 0
        assert result["CRITICAL"] == 0
    
    def test_get_icon_dict(self):
        """Test get_icon_dict returns correct structure."""
        result = Logges.LogStatus.get_icon_dict()
        
        assert isinstance(result, dict)
        assert "DEBUG" in result
        assert "INFO" in result
        assert "WARNING" in result
        assert "ERROR" in result
        assert "CRITICAL" in result
