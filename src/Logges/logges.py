"""An ultimate logging tool for python.

@package: Logges
@authors: Serkan UYSAL, Özkan UYSAL
@date: 2022
@mails: uysalserkan08@gmail.com, ozkan.uysal.2009@hotmail.com

DEPRECATION NOTICE:
The static Logges class API is deprecated and will be removed in version 3.0.
Please migrate to the new Logger class:

Old API (deprecated):
    from Logges import Logges
    Logges.setup(logname="myapp")
    Logges.log("message", Logges.LogStatus.ERROR)

New API (recommended):
    from Logges import get_logger, LogLevel
    logger = get_logger("myapp")
    logger.error("message")
"""

import os
import sys
import warnings
from ast import literal_eval
from enum import Enum
from pathlib import Path
from shutil import copy2
from typing import Dict, List, Union, Optional
from zipfile import ZipFile

from .utils import extract_logs
from .utils import get_current_time_HM
from .utils import get_daily_log_file_name
from .utils import get_log_info
from .utils import get_saving_path
from .utils import to_markdown
from .utils import to_pdf

# Import new logger components
from .logger import Logger as NewLogger
from .config import LogConfig, LogLevel

FILENAME = None
SAVINGPATH = None
STATUS_LEVEL = None
IGNORE_FILES_AND_DIRS = []

# Global instance for backward compatibility
_COMPAT_LOGGER: Optional[NewLogger] = None


class Logges:
    """The best logging tool in the world :D.

    DEPRECATED: This static API is deprecated. Use the new Logger class instead.

    You have to initial `setup` method with run script and set as `setup(__file__)`.

    Main method is `log` and that have 3 argument, please check its docstring.

    You can export you logs with `to_pdf()` and `to_markdown()`,
    if you want to just print the logs, use `console_data()` method.
    """

    class LogStatus(Enum):
        """Log types.

        `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
        """

        DEBUG = 0
        INFO = 1
        WARNING = 2
        ERROR = 3
        CRITICAL = 4

        @staticmethod
        def get_blank_dict() -> Dict[str, int]:
            """Convert Types to dictionary version."""
            int_status_dict = {
                "DEBUG": 0,
                "INFO": 0,
                "WARNING": 0,
                "ERROR": 0,
                "CRITICAL": 0,
            }
            return int_status_dict

        @staticmethod
        def get_icon_dict() -> Dict[str, str]:
            """Convert Types to dictionary version."""
            icon_status_dict = {
                "DEBUG": ":bulb:",
                "INFO": ":passport_control:",
                "WARNING": ":vs:",
                "ERROR": ":sos:",
                "CRITICAL": ":cop:",
            }
            return icon_status_dict

        def to_new_level(self) -> LogLevel:
            """Convert old LogStatus to new LogLevel.

            Returns:
                Corresponding LogLevel enum value
            """
            mapping = {
                0: LogLevel.DEBUG,
                1: LogLevel.INFO,
                2: LogLevel.WARNING,
                3: LogLevel.ERROR,
                4: LogLevel.CRITICAL,
            }
            if self.value not in mapping:
                import warnings

                warnings.warn(
                    f"Unknown log status value {self.value}, defaulting to INFO",
                    RuntimeWarning,
                    stacklevel=2,
                )
                return LogLevel.INFO
            return mapping[self.value]

    @staticmethod
    def setup(
        logname: str = None, status_level: LogStatus = LogStatus.ERROR, print_status: bool = True
    ) -> None:
        """Set the environment.

        DEPRECATED: Use Logger class instead.

        Set up environment and setting the logfile name.
        If you don't enter any name, the log name will be executing script name.

        Parameters:
            logname `str`: It defines your log file name.
            status_level `LogStatus`: If status equal or greater than parameter, automatically print it.
            Default value is `LogStatus.ERROR`
            print_status `bool`: Show on console log status.

        Return:
            None
        """
        warnings.warn(
            "Logges.setup() is deprecated. Use Logger class instead:\n"
            "  from Logges import get_logger\n"
            "  logger = get_logger('myapp')",
            DeprecationWarning,
            stacklevel=2,
        )

        os.environ["print_status"] = str(print_status)
        global FILENAME, SAVINGPATH, STATUS_LEVEL, _COMPAT_LOGGER
        STATUS_LEVEL = status_level.value
        filepath = sys._getframe().f_back.f_code.co_filename
        abs_filepath = os.path.abspath(filepath)
        if logname:
            FILENAME = logname
        else:
            FILENAME = os.path.split(abs_filepath)[1].split(".py")[0]
        SAVINGPATH = os.path.split(abs_filepath)[0]

        # Create new logger instance for compatibility
        try:
            config = LogConfig(
                name=FILENAME,
                level=status_level.to_new_level(),
                log_dir=Path(SAVINGPATH),
                print_to_console=print_status,
            )
            _COMPAT_LOGGER = NewLogger(config)
        except Exception:
            # If new logger fails, fall back to old behavior
            pass

    @staticmethod
    def _write_logs(msg: str) -> None:
        """write_logs method called by `logs` method for writting all logs to a file. You do not need this method.

        DEPRECATED: Internal method, will be removed.

        Parameters:
            msg `str`: A string that contains all log informations, separated by new line character.

        Return:
            None
        """
        global FILENAME, STATUS_LEVEL
        filename = get_daily_log_file_name(filename=FILENAME)
        log_dir = os.path.join(SAVINGPATH, filename)

        # Use context manager for proper resource management
        try:
            with open(log_dir, "a") as log_file:
                log_file.write(msg + "\n")
        except (IOError, OSError) as e:
            print(f"Error writing to log file: {e}", file=sys.stderr)

    @staticmethod
    def ignore_files(name: Union[str, List[str]]) -> None:
        """Ignore logs at files or directories. BE CAREFUL WHEN YOU IGNORE A FILE.

        Parameters:
            name `str or List`: Script name or directory of scripts.
        """
        global IGNORE_FILES_AND_DIRS
        if isinstance(name, List):
            for each_name in name:
                tmp = each_name.lower()
                if tmp not in IGNORE_FILES_AND_DIRS:
                    IGNORE_FILES_AND_DIRS.append(tmp)
        else:
            if name.lower() not in IGNORE_FILES_AND_DIRS:
                IGNORE_FILES_AND_DIRS.append(name.lower())

        # Update compat logger if it exists
        if _COMPAT_LOGGER:
            _COMPAT_LOGGER.config.ignored_files = IGNORE_FILES_AND_DIRS

    @staticmethod
    def log(msg: Union[str, any], status: LogStatus = LogStatus.DEBUG) -> None:
        r"""Log a string with status message, please do not use `\n` character in your strigs.

        DEPRECATED: Use logger.info(), logger.error(), etc. instead.

        Parameters:
            msg `str`: A string, showing on your report.
            status `LogStatus`: `Default is `DEBUG`.
            print_log `bool`: If you set that parameter True, print that log, default is False.

        Return:
            None
        """
        # Try to use new logger if available
        if _COMPAT_LOGGER:
            try:
                _COMPAT_LOGGER.log(msg, status.to_new_level())
                return
            except Exception:
                pass  # Fall back to old implementation

        # Old implementation
        print_log = literal_eval(os.environ.get("print_status", "True"))

        global IGNORE_FILES_AND_DIRS
        cur_time = get_current_time_HM()
        if not isinstance(msg, str):
            msg = str(msg)

        filepath, funct = get_log_info()

        if any(
            True if each_ignored in filepath.lower() else False
            for each_ignored in IGNORE_FILES_AND_DIRS
        ):
            return

        filename = os.path.split(filepath)[1]

        msg = f"[{cur_time}] [{status.name.center(10)}] [{filename}] [{funct}]: {msg}"

        if print_log:
            print(msg)
        elif status.value >= STATUS_LEVEL:
            print(msg)

        Logges._write_logs(msg=msg)

    @staticmethod
    def in_log(keyword: Union[str, List[str]]) -> bool:
        """Check if keyword(s) is logged in log file or not.

        Be aware of that, if log file has too many log row, this operation may take some time.

        Parameters:
            keyword `str or List of str`: It defines your searching keyword(s).

        Return:
            condition `bool`: Contains all True / not contains all False.
        """
        global FILENAME, SAVINGPATH
        filename = get_daily_log_file_name(filename=FILENAME)
        file_dir = SAVINGPATH
        full_logfile_path = os.path.join(file_dir, filename)

        try:
            with open(full_logfile_path, "r") as file:
                (
                    _,
                    _,
                    _,
                    _,
                    _log_message_list,
                ) = extract_logs(logs=file)
        except (IOError, OSError):
            return False

        if isinstance(keyword, str):
            for each_log in _log_message_list:
                if keyword in each_log:
                    return True
            return False
        else:
            for each_log in _log_message_list:
                counter = 0
                for each_keyword in keyword:
                    if each_keyword in each_log:
                        counter += 1
                    if counter == len(keyword):
                        return True
            return False

    @staticmethod
    def export(
        markdown: bool = False,
        pdf: bool = False,
        log: bool = True,
        zip: bool = False,
    ) -> None:
        """EXPORT."""
        global SAVINGPATH, FILENAME
        lib_path = get_saving_path()
        full_filename = get_daily_log_file_name(filename=FILENAME)
        copy2(
            src=os.path.join(SAVINGPATH, full_filename),
            dst=os.path.join(lib_path, full_filename),
        )
        if markdown:
            Logges._to_markdown()
        if pdf:
            Logges._to_pdf()
        if zip:
            zip_name = os.path.join(SAVINGPATH, FILENAME + ".zip")

            with ZipFile(file=zip_name, mode="w") as zipfile:
                if markdown:
                    filename = get_daily_log_file_name(
                        filename=FILENAME,
                        markdown=True,
                    )
                    file = os.path.join(SAVINGPATH, filename)
                    zipfile.write(file)
                    os.remove(file)
                if markdown:
                    filename = get_daily_log_file_name(
                        filename=FILENAME,
                        pdf=True,
                    )
                    file = os.path.join(SAVINGPATH, filename)
                    zipfile.write(file)
                    os.remove(file)
                if log:
                    filename = get_daily_log_file_name(
                        filename=FILENAME,
                    )
                    file = os.path.join(SAVINGPATH, filename)
                    zipfile.write(file)
                    os.remove(file)

        if not log:
            # Preserve log file at library director
            os.remove(os.path.join(SAVINGPATH, FILENAME))

    @staticmethod
    def _to_markdown() -> None:
        """Convert days logs as markdown file.."""
        global FILENAME, SAVINGPATH
        to_markdown(
            script_name=FILENAME,
            saving_path=SAVINGPATH,
            status_dict=Logges.LogStatus.get_blank_dict(),
            status_icons=Logges.LogStatus.get_icon_dict(),
        )

    @staticmethod
    def _to_pdf() -> None:
        """Convert logs to pdf file with day logs."""
        global FILENAME, SAVINGPATH
        to_pdf(
            script_name=FILENAME,
            saving_path=SAVINGPATH,
            status_dict=Logges.LogStatus.get_blank_dict(),
        )
