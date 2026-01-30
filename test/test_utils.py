"""Tests for Logges utility functions."""
from pathlib import Path

import pytest

from Logges.utils import (
    extract_logs,
    get_current_platform_name,
    get_current_time_HM,
    get_daily_log_file_name,
)


class TestGetCurrentPlatformName:
    """Test get_current_platform_name function."""
    
    def test_returns_string(self):
        """Test that function returns a string."""
        result = get_current_platform_name()
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_returns_valid_platform(self):
        """Test that function returns a valid platform name."""
        result = get_current_platform_name()
        valid_platforms = ["Linux", "Darwin", "Windows", "Java"]
        # At least one should match
        assert any(platform in result for platform in valid_platforms)


class TestGetCurrentTimeHM:
    """Test get_current_time_HM function."""
    
    def test_returns_string(self):
        """Test that function returns a string."""
        result = get_current_time_HM()
        assert isinstance(result, str)
    
    def test_time_format(self):
        """Test that time is in correct format HH:MM:SS."""
        result = get_current_time_HM()
        parts = result.split(":")
        
        assert len(parts) == 3
        assert len(parts[0]) == 2  # Hours
        assert len(parts[1]) == 2  # Minutes
        assert len(parts[2]) == 2  # Seconds
        
        # All parts should be numeric
        for part in parts:
            assert part.isdigit()


class TestGetDailyLogFileName:
    """Test get_daily_log_file_name function."""
    
    def test_default_log_extension(self):
        """Test that default extension is .log."""
        result = get_daily_log_file_name("test_script")
        assert result.endswith(".log")
        assert "test_script" in result
    
    def test_markdown_extension(self):
        """Test that markdown=True gives .md extension."""
        result = get_daily_log_file_name("test_script", markdown=True)
        assert result.endswith(".md")
        assert "test_script" in result
    
    def test_pdf_extension(self):
        """Test that pdf=True gives .pdf extension."""
        result = get_daily_log_file_name("test_script", pdf=True)
        assert result.endswith(".pdf")
        assert "test_script" in result
    
    def test_pdf_priority_over_markdown(self):
        """Test that pdf takes priority over markdown."""
        result = get_daily_log_file_name("test_script", markdown=True, pdf=True)
        assert result.endswith(".pdf")
    
    def test_includes_date(self):
        """Test that filename includes date in YYYY-MM-DD format."""
        result = get_daily_log_file_name("test_script")
        
        # Should have date prefix like 2026-01-30_
        parts = result.split("_")
        date_part = parts[0]
        
        # Check date format
        date_components = date_part.split("-")
        assert len(date_components) == 3
        assert len(date_components[0]) == 4  # Year
        assert len(date_components[1]) == 2  # Month
        assert len(date_components[2]) == 2  # Day


class TestExtractLogs:
    """Test extract_logs function."""
    
    def test_extract_valid_logs(self, sample_log_file: Path):
        """Test extracting logs from valid log file."""
        with open(sample_log_file, "r") as f:
            (
                date_list,
                status_list,
                filename_list,
                function_list,
                msg_list,
            ) = extract_logs(f)
        
        assert len(date_list) == 5
        assert len(status_list) == 5
        assert len(filename_list) == 5
        assert len(function_list) == 5
        assert len(msg_list) == 5
    
    def test_extract_dates(self, sample_log_file: Path):
        """Test that dates are extracted correctly."""
        with open(sample_log_file, "r") as f:
            date_list, *_ = extract_logs(f)
        
        for date in date_list:
            # Should be in format [HH:MM:SS] (10 chars including brackets)
            assert len(date) == 10
            assert date.startswith("[")
            assert date[3] == ":"
            assert date[6] == ":"
    
    def test_extract_statuses(self, sample_log_file: Path):
        """Test that statuses are extracted correctly."""
        with open(sample_log_file, "r") as f:
            _, status_list, *_ = extract_logs(f)
        
        # Status extraction removes trailing ]
        expected_statuses = ["[DEBUG", "[INFO", "[WARNING", "[ERROR", "[CRITICAL"]
        assert status_list == expected_statuses
    
    def test_extract_messages(self, sample_log_file: Path):
        """Test that messages are extracted correctly."""
        with open(sample_log_file, "r") as f:
            *_, msg_list = extract_logs(f)
        
        assert " Debug message\n" in msg_list[0]
        assert " Info message\n" in msg_list[1]
        assert " Warning message\n" in msg_list[2]
        assert " Error message\n" in msg_list[3]
        assert " Critical message\n" in msg_list[4]
    
    def test_extract_empty_file(self, temp_dir: Path):
        """Test extracting from empty file."""
        empty_file = temp_dir / "empty.log"
        empty_file.write_text("")
        
        with open(empty_file, "r") as f:
            (
                date_list,
                status_list,
                filename_list,
                function_list,
                msg_list,
            ) = extract_logs(f)
        
        assert len(date_list) == 0
        assert len(status_list) == 0
        assert len(filename_list) == 0
        assert len(function_list) == 0
        assert len(msg_list) == 0
