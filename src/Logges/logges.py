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

from .utils import create_pie_chart
from .utils import extract_logs
from .utils import get_current_platform_name
from .utils import get_current_time_HM
from .utils import get_daily_log_file_name
from .utils import get_log_info
from .utils import get_saving_path
from .utils import to_pdf


FILENAME = None
SAVINGPATH = None

STATUS_LEVEL = None
IGNORE_FILES_AND_DIRS = []


class Logges:
    """The best logging tool in the world :D.

    You have to initial `setup` method with run script and set as `setup(__file__)`.

    Main method is `log` and that have 3 argument, please check its docstring.

    You can export you logs with `to_pdf()` and `to_markdown()`, if you want to just print the logs, use `console_data()` method.
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
    def setup(filepath) -> None:
        """You need to enter just `__file__` input to filepath argument. This method will name your logs as running script name.

        Return:
            None
        """
        global FILENAME, SAVINGPATH
        path = os.path.abspath(filepath)
        FILENAME = os.path.split(path)[1].split(".py")[0]
        SAVINGPATH = os.path.split(path)[0]

    @staticmethod
    def write_logs(msg: str) -> None:
        """write_logs method called by `logs` method for writting all logs to a file. You do not need this method.

        Parameters:
            msg `str`: A string that contains all log informations, separated by new line character.

        Return:
            None
        """
        filename = get_daily_log_file_name(filename=Logges.get_log_name())
        saving_dir = get_saving_path()
        log_dir = os.path.join(saving_dir, filename)
        log_file = open(f"{log_dir}", "a")
        log_file.writelines(msg + "\n")

    def get_status_message(status: int) -> str:
        """Hidden internal method, that returns the status to text.

        Parameters:
            status `int`: Status number 0 to 2.

        Return:
            status_text `str`: What is status name.
        """
        status_text = f"[{STATUS[status]}] "
        return status_text

    @staticmethod
    def get_log_name() -> str:
        """Actually this method do nothing."""
        global FILENAME
        return FILENAME

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
            logs `str`: A string, showing on your report.
            status `int`: `0` is info, `1` is warning and `2` is error, default is 0.
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
            True if each_ignored in filepath else False
            for each_ignored in IGNORE_FILES_AND_DIRS
        ):
            return

        filename = os.path.split(filepath)[1]

        msg = f"[{cur_time}] [{status.name:8s}] [{filename}] [{funct}]: {msg}"

        if print_log:
            print(msg)

        Logges.write_logs(msg=msg)

    @staticmethod
    def export(markdown: bool = False, pdf: bool = False, log: bool = True) -> None:
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
        if not log:
            # Preserve log file at library directory
            os.remove(os.path.join(SAVINGPATH, FILENAME))

    @staticmethod
    def _to_markdown() -> None:
        """Convert days logs as markdown file.."""
        global FILENAME, SAVINGPATH

        status_icons = Logges.LogStatus.get_icon_dict()
        md_file = os.path.join(
            SAVINGPATH, get_daily_log_file_name(filename=FILENAME, markdown=True)
        )
        markdown_file = open(md_file, "w")

        filename = get_daily_log_file_name(filename=FILENAME)
        file_dir = SAVINGPATH
        full_logfile_path = os.path.join(file_dir, filename)

        only_filename = "_".join(filename.split("_")[1:]) + ".py".replace(".log", "")
        file_date = filename.split("_")[0]

        # Fix Windows Problems.
        if get_current_platform_name() == "Windows":
            only_filename = os.path.split(only_filename)[1]

        markdown_file.writelines(
            f"# {only_filename} {file_date} Logs :see_no_evil: :hear_no_evil: :speak_no_evil:\n"
        )
        markdown_file.writelines("![](pie_chart.png)\n")
        markdown_file.writelines(
            "|TIME|STATUS|FILENAME|FUNCTION|MESSAGE|\n| :--: | :--: | :--: | :--: | :--: |\n"
        )

        # Split Strings.
        file = open(full_logfile_path, "r")
        (
            _date_list,
            _status_list,
            _filename_list,
            _functname_list,
            _log_message_list,
        ) = extract_logs(logs=file)

        status_dict = Logges.LogStatus.get_blank_dict()
        # Write logs in markdown file.
        for index, _ in enumerate(_log_message_list):
            log_status_clear = _status_list[index].replace("[", "").replace("]", "")
            status_dict[log_status_clear] += 1

            try:
                markdown_file.writelines(
                    "|{}|{}|{}|{}|{}|".format(
                        _date_list[index],
                        status_icons[log_status_clear],
                        _filename_list[index],
                        _functname_list[index],
                        _log_message_list[index].replace("\n", " "),
                    )
                )
                markdown_file.write("\n")
            except KeyError:
                raise ("Please check your icon.")

        # Write signature
        markdown_file.writelines(
            "All right reserved 2022 &copy;&nbsp; [Logges](https://github.com/uysalserkan/Logges) - \
*[uysalserkan](https://github.com/uysalserkan/) & [Ozkan](https://github.com/ozkanuysal)*\n"
        )

        # Create chart
        create_pie_chart(
            saving_path=SAVINGPATH,
            status_dict=status_dict,
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
