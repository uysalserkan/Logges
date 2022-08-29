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
from typing import Dict, Union

from .utils import console_data
from .utils import create_pie_chart
from .utils import get_current_platform_name
from .utils import get_current_time_HM
from .utils import get_daily_log_file_name
from .utils import get_saving_path
from .utils import to_pdf

FILENAME = None
SAVINGPATH = None
STATUS_LEVEL = None


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
        def get_int_dict() -> Dict[str, int]:
            """Convert Types to dictionary version."""
            int_status_dict = {
                "DEBUG": 0,
                "INFO": 1,
                "WARNING": 2,
                "ERROR": 3,
                "CRITICAL": 4,
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
    def log(msg: Union[str, any],
            status: LogStatus = LogStatus.DEBUG,
            print_log: bool = False) -> None:
        r"""Log a string with status message, please do not use `\n` character in your strigs.

        Parameters:
            msg `str`: A string, showing on your report.
            status `LogStatus`: `Default is `DEBUG`.
            print_log `bool`: If you set that parameter True, print that log, default is False.

        Return:
            None
        """
        cur_time = get_current_time_HM()
        if not isinstance(msg, str):
            msg = str(msg)

        msg = f"[{cur_time}] [{status.name:8s}]: {msg}"

        if print_log:
            print(msg)
        elif status.value >= STATUS_LEVEL:
            print(msg)

        Logges._write_logs(msg=msg)

    @staticmethod
    def export(markdown: bool = False,
               pdf: bool = False,
               log: bool = True) -> None:
        """EXPORT."""
        if markdown:
            Logges._to_markdown()
        if pdf:
            Logges._to_pdf()
        lib_path = get_saving_path()
        copy2(src=os.path.join(SAVINGPATH, FILENAME),
              dst=os.path.join(lib_path, FILENAME))
        if not log:
            # Preserve log file at library directory
            os.remove(os.path.join(SAVINGPATH, FILENAME))

    @staticmethod
    def _to_markdown() -> None:
        """Convert days logs as markdown file.."""
        global FILENAME

        icons = Logges.LogStatus.get_icon_dict()
        type_counter = [0, 0, 0, 0, 0]
        md_file = os.path.join(
            SAVINGPATH,
            get_daily_log_file_name(filename=FILENAME, markdown=True))
        markdown_file = open(md_file, "w")

        filename = get_daily_log_file_name(filename=FILENAME)
        file_dir = get_saving_path()
        log_path = os.path.join(file_dir, filename)
        with open(log_path, "r") as file:
            logs = file.readlines()
            file.close()
        only_filename = "_".join(filename.split("_")[1:]) + ".py".replace(
            ".log", "")
        file_date = filename.split("_")[0]

        if get_current_platform_name() == "Windows":
            only_filename = os.path.split(only_filename)[1]
        markdown_file.writelines(
            f"# {only_filename} {file_date} Logs :see_no_evil: :hear_no_evil: :speak_no_evil:\n"
        )
        markdown_file.writelines("![](pie_chart.png)\n")
        markdown_file.writelines(
            "|TYPE|TIME|MESSAGE|\n| :--: | :--: | :--: |\n")
        for each_log in logs[::-1]:
            log_type = (each_log.split("\t")[0].split(" ")[0].replace(
                "[", "").replace("]", ""))
            if log_type == list(icons.keys())[0]:
                type_counter[0] += 1
            elif log_type == list(icons.keys())[1]:
                type_counter[1] += 1
            elif log_type == list(icons.keys())[2]:
                type_counter[2] += 1

            log_time = (each_log.split("\t")[0].split(" ")[1].replace(
                "[", "").replace("]", "")[0:-1])
            log_msg = each_log.split("\t")[1]
            log_msg.replace("\n", "")
            try:
                markdown_file.writelines(
                    f"|{icons[log_type]} | {log_time} | {log_msg.strip()}| ")
                markdown_file.writelines("\n")
            except KeyError:
                raise ("Please check your icon.")
        markdown_file.writelines(
            "All right reserved 2022 &copy;&nbsp; [Logges](https://github.com/uysalserkan/Logges) - \
*[uysalserkan](https://github.com/uysalserkan/) & [Ozkan](https://github.com/ozkanuysal)*\n"
        )
        create_pie_chart(
            saving_path=SAVINGPATH,
            info_size=type_counter[0],
            warning_size=type_counter[1],
            error_size=type_counter[2],
        )

    @staticmethod
    def console_data() -> None:
        """Fill the beautiful table with days logs."""
        global FILENAME
        console_data(script_name=FILENAME)

    @staticmethod
    def _to_pdf() -> None:
        """Convert logs to pdf file with day logs."""
        global FILENAME
        to_pdf(script_name=FILENAME, saving_path=SAVINGPATH)
