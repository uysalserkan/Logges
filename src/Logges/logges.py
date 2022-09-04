"""An ultimate logging tool for python.

@package: Logges
@authors: Serkan UYSAL, Özkan UYSAL
@date: 2022
@mails: uysalserkan08@gmail.com, ozkan.uysal.2009@hotmail.com
"""
import os
import sys
from enum import Enum
from shutil import copy2
from typing import Dict
from typing import List
from typing import Union
from zipfile import ZipFile

from .utils import extract_logs
from .utils import get_current_time_HM
from .utils import get_daily_log_file_name
from .utils import get_log_info
from .utils import get_saving_path
from .utils import to_markdown
from .utils import to_pdf

FILENAME = None
SAVINGPATH = None
STATUS_LEVEL = None
IGNORE_FILES_AND_DIRS = []


class Logges:
    """The best logging tool in the world :D.

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

    @staticmethod
    def setup(logname: str = None, status_level: LogStatus = LogStatus.ERROR) -> None:
        """Set the environment.

        Set up environment and setting the logfile name.
        If you don't enter any name, the log name will be executing script name.

        Parameters:
            logname `str`: It defines your log file name.
            status_level `LogStatus`: If status equal or greater than parameter, automatically print it.
            Default value is `LogStatus.ERROR`

        Return:
            None
        """
        global FILENAME, SAVINGPATH, STATUS_LEVEL
        STATUS_LEVEL = status_level.value
        filepath = sys._getframe().f_back.f_code.co_filename
        abs_filepath = os.path.abspath(filepath)
        if logname:
            FILENAME = logname
        else:
            FILENAME = os.path.split(abs_filepath)[1].split(".py")[0]
        SAVINGPATH = os.path.split(abs_filepath)[0]

    @staticmethod
    def _write_logs(msg: str) -> None:
        """write_logs method called by `logs` method for writting all logs to a file. You do not need this method.

        Parameters:
            msg `str`: A string that contains all log informations, separated by new line character.

        Return:
            None
        """
        global FILENAME, STATUS_LEVEL
        filename = get_daily_log_file_name(filename=FILENAME)
        # saving_dir = get_saving_path()
        log_dir = os.path.join(SAVINGPATH, filename)
        log_file = open(f"{log_dir}", "a")
        log_file.writelines(msg + "\n")
        log_file.close()

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

    @staticmethod
    def log(
        msg: Union[str, any],
        status: LogStatus = LogStatus.DEBUG,
        print_log: bool = False,
    ) -> None:
        r"""Log a string with status message, please do not use `\n` character in your strigs.

        Parameters:
            msg `str`: A string, showing on your report.
            status `LogStatus`: `Default is `DEBUG`.
            print_log `bool`: If you set that parameter True, print that log, default is False.

        Return:
            None
        """
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

        msg = f"[{cur_time}] [{status.name:8s}] [{filename}] [{funct}]: {msg}"

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

        file = open(full_logfile_path, "r")
        (
            _,
            _,
            _,
            _,
            _log_message_list,
        ) = extract_logs(logs=file)

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
