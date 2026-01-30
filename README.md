git status```txt
LLLLLLLLLLL                                                                                            SSSSSSSSSSSSSSS
L:::::::::L                                                                                          SS:::::::::::::::S
L:::::::::L                                                                                         S:::::SSSSSS::::::S
LL:::::::LL                                                                                         S:::::S     SSSSSSS
  L:::::L                  ooooooooooo      ggggggggg   ggggg   ggggggggg   ggggg    eeeeeeeeeeee   S:::::S
  L:::::L                oo:::::::::::oo   g:::::::::ggg::::g  g:::::::::ggg::::g  ee::::::::::::ee S:::::S
  L:::::L               o:::::::::::::::o g:::::::::::::::::g g:::::::::::::::::g e::::::eeeee:::::eeS::::SSSS
  L:::::L               o:::::ooooo:::::og::::::ggggg::::::ggg::::::ggggg::::::gge::::::e     e:::::e SS::::::SSSSS
  L:::::L               o::::o     o::::og:::::g     g:::::g g:::::g     g:::::g e:::::::eeeee::::::e   SSS::::::::SS
  L:::::L               o::::o     o::::og:::::g     g:::::g g:::::g     g:::::g e:::::::::::::::::e       SSSSSS::::S
  L:::::L               o::::o     o::::og:::::g     g:::::g g:::::g     g:::::g e::::::eeeeeeeeeee             S:::::S
  L:::::L         LLLLLLo::::o     o::::og::::::g    g:::::g g::::::g    g:::::g e:::::::e                      S:::::S
LL:::::::LLLLLLLLL:::::Lo:::::ooooo:::::og:::::::ggggg:::::g g:::::::ggggg:::::g e::::::::e         SSSSSSS     S:::::S
L::::::::::::::::::::::Lo:::::::::::::::o g::::::::::::::::g  g::::::::::::::::g  e::::::::eeeeeeee S::::::SSSSSS:::::S
L::::::::::::::::::::::L oo:::::::::::oo   gg::::::::::::::g   gg::::::::::::::g   ee:::::::::::::e S:::::::::::::::SS
LLLLLLLLLLLLLLLLLLLLLLLL   ooooooooooo       gggggggg::::::g     gggggggg::::::g     eeeeeeeeeeeeee  SSSSSSSSSSSSSSS
                                                     g:::::g             g:::::g
                                         gggggg      g:::::g gggggg      g:::::g
                                         g:::::gg   gg:::::g g:::::gg   gg:::::g
                                          g::::::ggg:::::::g  g::::::ggg:::::::g
                                           gg:::::::::::::g    gg:::::::::::::g
                                             ggg::::::ggg        ggg::::::ggg
                                                gggggg              gggggg

```

![PyPI - Downloads](https://img.shields.io/pypi/dm/logges?label=Downloads&logo=monthly_download&style=flat-square) ![Scrutinizer code quality (GitHub/Bitbucket)](https://img.shields.io/scrutinizer/quality/b/uysalserkan/logges/main?style=flat-square) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/uysalserkan/logges?style=flat-square) ![Scrutinizer coverage (GitHub/BitBucket)](https://img.shields.io/scrutinizer/coverage/b/uysalserkan/logges/main?style=flat-square) ![GitHub](https://img.shields.io/github/license/uysalserkan/logges?style=flat-square) ![GitHub forks](https://img.shields.io/github/forks/uysalserkan/logges?style=social) ![GitHub Repo stars](https://img.shields.io/github/stars/uysalserkan/logges?style=social) ![PyPI](https://img.shields.io/pypi/v/logges?style=flat-square)

**A modern, production-ready Python logging library with rich features and an easy-to-use API.**

---

## 📋 Table of Contents

- [About](#about-speaker)
- [What's New in v2.4](#whats-new-in-v24-sparkles)
- [Installation](#installation-open_file_folder)
- [Quick Start](#quick-start-rocket)
  - [Modern API (Recommended)](#modern-api-recommended)
  - [Legacy API (Deprecated)](#legacy-api-deprecated)
- [Features](#features-star2)
- [Usage Guide](#usage-guide-memo)
  - [Basic Logging](#basic-logging)
  - [Configuration](#configuration)
  - [Log Levels](#log-levels)
  - [Context Managers](#context-managers)
  - [Multiple Loggers](#multiple-loggers)
  - [Custom Handlers](#custom-handlers)
- [Export Options](#export-options-package)
- [CLI Tool](#cli-tool-clipboard)
- [Migration Guide](#migration-guide-arrow_right)
- [API Reference](#api-reference-books)
- [Best Practices](#best-practices-bulb)
- [Troubleshooting](#troubleshooting-wrench)
- [Contributing](#contributing-handshake)
- [License](#license-page_facing_up)
- [Contact](#contact-tophat)

---

## About :speaker:

**Logges** is a powerful, production-ready logging library for Python that provides a clean, modern API while maintaining backward compatibility. Whether you need simple file logging or complex multi-destination log management, Logges has you covered.

### Why Logges?

- ✅ **Modern & Clean API** - Simple, intuitive interface following Python best practices
- ✅ **Production-Ready** - Thread-safe, secure, and thoroughly tested
- ✅ **Rich Features** - Export logs as PDF, Markdown, or Zip archives
- ✅ **Type-Safe** - Full type hints for better IDE support
- ✅ **Flexible** - Extensible handler pattern for custom log destinations
- ✅ **CLI Tool** - Powerful command-line interface for log analysis
- ✅ **Backward Compatible** - Seamless migration path from older versions

---

## What's New in v2.4 :sparkles:

**Major architectural refactoring with enhanced security and performance!**

### 🎉 New Modern API
- **Instance-based design** - No more global state, fully thread-safe
- **Context manager support** - Automatic resource cleanup
- **Handler pattern** - Easily extend with custom log destinations
- **Enhanced type hints** - Better IDE autocomplete and type checking

### 🔒 Security Improvements
- Input validation to prevent path traversal attacks
- Message size limits to prevent memory exhaustion
- Comprehensive configuration validation
- Multi-level error handling with fallbacks

### 📈 Performance & Reliability
- Improved frame introspection with fallback mechanisms
- Early returns for better performance
- Graceful error handling throughout
- 40% test coverage (75% for new code)

### 🔄 Backward Compatibility
- Old API continues to work with deprecation warnings
- Smooth migration path to new API
- All existing code remains functional

👉 **See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design documentation**
👉 **See [CODE_REVIEW_IMPLEMENTATION.md](CODE_REVIEW_IMPLEMENTATION.md) for security improvements**

---

## Installation :open_file_folder:

### Using pip

```bash
pip install Logges
```

### Using poetry

```bash
poetry add Logges
```

### From source

```bash
git clone https://github.com/uysalserkan/Logges.git
cd Logges
pip install -e .
```

### Requirements

- Python 3.10 or higher
- Dependencies: `matplotlib`, `rich`, `reportlab`, `click`

---

## Quick Start :rocket:

### Modern API (Recommended)

The new modern API provides a clean, Pythonic interface with full type safety:

```python
from Logges import get_logger

# Create a logger
logger = get_logger("myapp")

# Log messages at different levels
logger.debug("Starting application...")
logger.info("Application initialized successfully")
logger.warning("Configuration file not found, using defaults")
logger.error("Failed to connect to database")
logger.critical("System is shutting down!")

# Always close when done
logger.close()
```

**Better: Use as a context manager** (automatic cleanup):

```python
from Logges import get_logger

with get_logger("myapp") as logger:
    logger.info("Application started")
    logger.error("An error occurred")
# Logger automatically closed here
```

### Legacy API (Deprecated)

The old API still works but shows deprecation warnings:

```python
from Logges import Logges

# Setup
Logges.setup(logname="myapp", status_level=Logges.LogStatus.ERROR)

# Log messages
Logges.log("Error occurred", Logges.LogStatus.ERROR)
Logges.log("Debug info", Logges.LogStatus.DEBUG)
```

⚠️ **Note**: The legacy API is deprecated and will be removed in v3.0. Please migrate to the modern API.

---

## Features :star2:

### Core Features

| Feature | Description |
|---------|-------------|
| 🎯 **Multiple Log Levels** | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| 📁 **File Logging** | Automatic daily log rotation with timestamps |
| 🖥️ **Console Output** | Colored console output with customizable formatting |
| 📦 **Export Formats** | Export logs as PDF, Markdown, or Zip archives |
| 🔍 **Log Search** | Built-in CLI tool for searching and filtering logs |
| 🎨 **Customizable** | Flexible configuration and custom handlers |
| 🔒 **Secure** | Input validation and memory protection |
| 🧵 **Thread-Safe** | Multiple independent logger instances |
| 📊 **Statistics** | Log analysis and visualization |

### Advanced Features

- **Custom Handlers**: Easily extend with database, network, or custom handlers
- **Context Managers**: Automatic resource cleanup
- **Type Safety**: Full type hints for better IDE support
- **Error Recovery**: Multi-level fallback error handling
- **Message Limits**: Configurable size limits to prevent memory issues
- **File Filtering**: Ignore logs from specific files or directories
- **Structured Logging**: Support for additional metadata via `**extra` parameters

---

## Usage Guide :memo:

### Basic Logging

#### Simple Logging

```python
from Logges import get_logger

logger = get_logger("myapp")
logger.info("Hello, Logges!")
logger.close()
```

#### Logging with Context Manager

```python
from Logges import get_logger

with get_logger("myapp") as logger:
    logger.info("This is better - automatic cleanup!")
```

#### Logging Different Types

```python
with get_logger("myapp") as logger:
    logger.info("String message")
    logger.info(123)  # Numbers
    logger.info([1, 2, 3])  # Lists
    logger.info({"key": "value"})  # Dictionaries
    logger.info(Exception("error"))  # Exceptions
```

### Configuration

#### Basic Configuration

```python
from Logges import get_logger, LogLevel

logger = get_logger(
    name="myapp",
    level=LogLevel.DEBUG,  # Log everything
    log_dir="/var/log/myapp"  # Custom log directory
)
```

#### Advanced Configuration

```python
from Logges import Logger, LogConfig, LogLevel
from pathlib import Path

config = LogConfig(
    name="myapp",
    level=LogLevel.INFO,
    log_dir=Path("./logs"),
    print_to_console=True,
    daily_rotation=True,
    ignored_files=["test_", "debug_"],
    max_message_size=10_000,  # 10KB per message
)

with Logger(config) as logger:
    logger.info("Configured logger ready!")
```

### Log Levels

Logges provides five standard log levels:

```python
from Logges import get_logger, LogLevel

with get_logger("myapp", level=LogLevel.DEBUG) as logger:
    logger.debug("Detailed information for debugging")
    logger.info("General informational messages")
    logger.warning("Warning messages for potentially harmful situations")
    logger.error("Error messages for serious problems")
    logger.critical("Critical messages for very serious errors")
```

**Level Hierarchy**: DEBUG < INFO < WARNING < ERROR < CRITICAL

Messages are only logged if their level is >= the configured minimum level.

### Context Managers

**Always prefer context managers** for automatic resource cleanup:

```python
from Logges import get_logger

# Good ✅
with get_logger("myapp") as logger:
    logger.info("Automatic cleanup")

# Less ideal ⚠️
logger = get_logger("myapp")
logger.info("Manual cleanup required")
logger.close()  # Don't forget this!
```

### Multiple Loggers

Create independent logger instances for different parts of your application:

```python
from Logges import get_logger

# Each logger is independent and thread-safe
auth_logger = get_logger("auth")
api_logger = get_logger("api")
db_logger = get_logger("database")

auth_logger.info("User logged in")
api_logger.info("API request received")
db_logger.error("Database connection failed")

# Clean up
auth_logger.close()
api_logger.close()
db_logger.close()
```

### Custom Handlers

Extend Logges with custom log destinations:

```python
from Logges import Logger, LogConfig
from Logges.handlers import LogHandler, FileHandler
from Logges.config import LogRecord

class DatabaseHandler(LogHandler):
    """Custom handler that writes logs to a database."""
    
    def emit(self, record: LogRecord, formatted_message: str) -> None:
        # Write to database
        db.insert_log(
            level=record.level.name,
            message=record.message,
            timestamp=record.timestamp,
            filename=record.filename
        )
    
    def close(self) -> None:
        db.close()

# Use custom handler
config = LogConfig(name="myapp")
logger = Logger(config, handlers=[
    FileHandler(Path("app.log")),
    DatabaseHandler(),
])
```

### Structured Logging

Add metadata to your logs:

```python
with get_logger("myapp") as logger:
    logger.info(
        "User action",
        user_id="12345",
        action="login",
        ip_address="192.168.1.1"
    )
```

### Filtering Logs

Ignore logs from specific files:

```python
from Logges import LogConfig, Logger

config = LogConfig(
    name="myapp",
    ignored_files=["test_", "debug_", "temp_"]  # Ignore test and debug files
)

with Logger(config) as logger:
    logger.info("This will be logged")
    # Logs from files matching patterns will be ignored
```

---

## Export Options :package:

### Export Logs to Different Formats

```python
from Logges import Logges

# Use legacy API for export functionality
Logges.setup(logname="myapp")
Logges.log("Important event", Logges.LogStatus.ERROR)

# Export as Markdown
Logges.export(markdown=True)

# Export as PDF
Logges.export(pdf=True)

# Export everything as Zip
Logges.export(markdown=True, pdf=True, log=True, zip=True)
```

Exported files include:
- **Markdown (.md)**: Easy to read, version-control friendly
- **PDF (.pdf)**: Professional reports with statistics and charts
- **Zip (.zip)**: Compressed archive of all formats

---

## CLI Tool :clipboard:

Logges includes a powerful command-line interface for log analysis:

### List Log Files

```bash
# List all logs
logges list

# Filter by date range
logges list --min-date 2024-01-01 --max-date 2024-12-31
```

### Show Log Contents

```bash
# Show a log file
logges show --file 2024-01-30_myapp.log

# Show local log file
logges show --file /path/to/myapp.log --local-file
```

### Search Logs

```bash
# Search for specific keywords
logges search --sentences "error,failed,exception"

# Filter by function
logges search --sentences "error" --functions "process_data"

# Filter by status level
logges search --sentences "error" --status "ERROR,CRITICAL"

# Filter by source file
logges search --sentences "error" --files "main.py"

# Export search results
logges search --sentences "error" --export --export-name "error_report"
```

### CLI Options

| Command | Options | Description |
|---------|---------|-------------|
| `list` | `--min-date`, `--max-date` | List log files with date filtering |
| `show` | `-f/--file`, `--local-file` | Display log file contents |
| `search` | `-sen/--sentences`, `-fun/--functions`, `-sta/--status`, `-fi/--files`, `-e/--export` | Search and filter logs |

---

## Migration Guide :arrow_right:

### From v2.3 or Earlier to v2.4

#### Step 1: Update Your Imports

**Old way:**
```python
from Logges import Logges
```

**New way:**
```python
from Logges import get_logger, LogLevel
```

#### Step 2: Replace setup() with get_logger()

**Old way:**
```python
Logges.setup(logname="myapp", status_level=Logges.LogStatus.ERROR)
```

**New way:**
```python
logger = get_logger("myapp", level=LogLevel.ERROR)
```

#### Step 3: Replace log() calls with level methods

**Old way:**
```python
Logges.log("Error occurred", Logges.LogStatus.ERROR)
Logges.log("Info message", Logges.LogStatus.INFO)
```

**New way:**
```python
logger.error("Error occurred")
logger.info("Info message")
```

#### Step 4: Add cleanup

**New way:**
```python
# Option 1: Manual cleanup
logger.close()

# Option 2: Context manager (recommended)
with get_logger("myapp") as logger:
    logger.error("Error occurred")
```

### Full Migration Example

**Before (v2.3):**
```python
from Logges import Logges

Logges.setup(logname="myapp", status_level=Logges.LogStatus.INFO)
Logges.ignore_files(["test_"])
Logges.log("Application started", Logges.LogStatus.INFO)
Logges.log("Error occurred", Logges.LogStatus.ERROR)
```

**After (v2.4):**
```python
from Logges import get_logger, LogLevel

with get_logger("myapp", level=LogLevel.INFO) as logger:
    # Note: File filtering should be set in LogConfig
    logger.info("Application started")
    logger.error("Error occurred")
```

**With full configuration:**
```python
from Logges import Logger, LogConfig, LogLevel
from pathlib import Path

config = LogConfig(
    name="myapp",
    level=LogLevel.INFO,
    ignored_files=["test_"],
    log_dir=Path("./logs")
)

with Logger(config) as logger:
    logger.info("Application started")
    logger.error("Error occurred")
```

---

## API Reference :books:

### Main Classes

#### `Logger`

The main logger class for modern API.

```python
class Logger:
    def __init__(self, config: LogConfig, handlers: Optional[list[LogHandler]] = None)
    def debug(self, message: str | Any, **extra: str) -> None
    def info(self, message: str | Any, **extra: str) -> None
    def warning(self, message: str | Any, **extra: str) -> None
    def error(self, message: str | Any, **extra: str) -> None
    def critical(self, message: str | Any, **extra: str) -> None
    def close(self) -> None
```

#### `LogConfig`

Configuration for a Logger instance.

```python
@dataclass
class LogConfig:
    name: str                           # Logger name (alphanumeric, -, _)
    level: LogLevel = LogLevel.INFO     # Minimum log level
    log_dir: Path = Path.cwd()          # Log directory
    print_to_console: bool = True       # Print to console
    daily_rotation: bool = True         # Create daily log files
    ignored_files: list[str] = []       # Files to ignore
    max_message_size: int = 10_000      # Max message size in bytes
```

#### `LogLevel`

Log severity levels (enum).

```python
class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
```

### Convenience Functions

#### `get_logger()`

Quick way to create a logger with default settings.

```python
def get_logger(
    name: str,
    level: LogLevel = LogLevel.INFO,
    log_dir: Optional[Path] = None
) -> Logger
```

### Handler Classes

#### `FileHandler`

Writes logs to a file.

```python
class FileHandler(LogHandler):
    def __init__(self, filepath: Path) -> None
```

#### `ConsoleHandler`

Writes logs to console (stdout/stderr).

```python
class ConsoleHandler(LogHandler):
    def __init__(self, use_stderr_for_errors: bool = True) -> None
```

### Exceptions

```python
class LoggesError(Exception)           # Base exception
class ConfigurationError(LoggesError)  # Configuration errors
class LogFileError(LoggesError)        # File operation errors
class HandlerError(LoggesError)        # Handler errors
```

---

## Best Practices :bulb:

### ✅ Do's

1. **Use context managers** for automatic cleanup
   ```python
   with get_logger("myapp") as logger:
       logger.info("Message")
   ```

2. **Use appropriate log levels**
   - DEBUG: Detailed diagnostic information
   - INFO: General informational messages
   - WARNING: Warning messages
   - ERROR: Error messages
   - CRITICAL: Critical failures

3. **Configure once, use everywhere**
   ```python
   config = LogConfig(name="myapp", level=LogLevel.INFO)
   logger = Logger(config)
   ```

4. **Use structured logging for metadata**
   ```python
   logger.info("User action", user_id="123", action="login")
   ```

5. **Create separate loggers for different components**
   ```python
   auth_logger = get_logger("auth")
   api_logger = get_logger("api")
   ```

### ❌ Don'ts

1. **Don't forget to close loggers** (unless using context managers)
   ```python
   # Bad ❌
   logger = get_logger("myapp")
   logger.info("Message")
   # Forgot logger.close()!
   ```

2. **Don't use print() for logging**
   ```python
   # Bad ❌
   print("User logged in")
   
   # Good ✅
   logger.info("User logged in")
   ```

3. **Don't log sensitive information**
   ```python
   # Bad ❌
   logger.info(f"Password: {password}")
   
   # Good ✅
   logger.info("User authenticated successfully")
   ```

4. **Don't use global loggers** (new API)
   ```python
   # Bad ❌
   LOGGER = get_logger("myapp")  # Global
   
   # Good ✅
   def get_app_logger():
       return get_logger("myapp")
   ```

---

## Troubleshooting :wrench:

### Common Issues

#### Issue: "Logger name contains invalid characters"

**Cause**: Logger names must only contain alphanumeric characters, hyphens, and underscores.

**Solution**:
```python
# Bad ❌
config = LogConfig(name="my/app")

# Good ✅
config = LogConfig(name="my-app")
```

#### Issue: "Cannot create log directory"

**Cause**: Insufficient permissions to create log directory.

**Solution**:
```python
# Use a directory you have write access to
config = LogConfig(name="myapp", log_dir=Path.home() / "logs")
```

#### Issue: Log messages are truncated

**Cause**: Messages exceed the maximum size limit (default 10KB).

**Solution**:
```python
# Increase the limit if needed
config = LogConfig(name="myapp", max_message_size=50_000)  # 50KB
```

#### Issue: Deprecation warnings from old API

**Cause**: Using the deprecated static `Logges` API.

**Solution**: Migrate to the modern API (see [Migration Guide](#migration-guide-arrow_right))

---

## Contributing :handshake:

We welcome contributions! Here's how you can help:

### Development Setup

```bash
# Clone the repository
git clone https://github.com/uysalserkan/Logges.git
cd Logges

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest test/ -v

# Run type checking
mypy src/Logges/

# Format code
black src/Logges/
ruff check src/Logges/
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src/Logges --cov-report=html

# Specific test file
pytest test/test_logger_new.py -v
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public APIs
- Add tests for new features
- Update documentation

---

## License :page_facing_up:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact :tophat:

**Maintainers:**
- [Serkan UYSAL](https://github.com/uysalserkan)
- [Özkan UYSAL](https://github.com/ozkanuysal)

**Links:**
- 🐛 [Report a Bug](https://github.com/uysalserkan/Logges/issues/new)
- 💡 [Request a Feature](https://github.com/uysalserkan/Logges/issues/new)
- 📖 [Documentation](https://github.com/uysalserkan/Logges)
- 💬 [Discussions](https://github.com/uysalserkan/Logges/discussions)

---

## Acknowledgments

Special thanks to all contributors and users who have helped make Logges better!

**Star ⭐ this repository if you find it helpful!**

---

<div align="center">

Made with ❤️ by the Logges team

[Back to Top ⬆️](#)

</div>
