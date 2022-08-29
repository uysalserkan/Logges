"""An ultimate logging tool for python.

@package: Logges
@authors: Serkan UYSAL, Özkan UYSAL
@date: 2022
@mails: uysalserkan08@gmail.com, ozkan.uysal.2009@hotmail.com
"""
import os

from .utils import console_data
from .utils import create_pie_chart
from .utils import get_current_platform_name
from .utils import get_current_time_HM
from .utils import get_daily_log_file_name
from .utils import get_saving_path
from .utils import to_pdf

STATUS = ["INFO", "WARNING", "ERROR"]
FILENAME = None
SAVINGPATH = None


class Logges:
    """The best logging tool in the world :D.

    You have to initial `setup` method with run script and set as `setup(__file__)`.

    Main method is `log` and that have 3 argument, please check its docstring.

    You can export you logs with `to_pdf()` and `to_markdown()`, if you want to just print the logs, use `console_data()` method.
    """

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
    def log(log: str, status: int = 0, print_log: bool = True) -> None:
        r"""Log a string with status message, please do not use `\n` character in your strigs.

        Parameters:
            logs `str`: A string, showing on your report.
            status `int`: `0` is info, `1` is warning and `2` is error, default is 0.
            print_log `bool`: If you set that parameter True, print that log, default is False.

        Return:
            None
        """
        cur_time = get_current_time_HM()
        status = Logges.get_status_message(status=status)
        msg = f"{status}{cur_time}\t{log}"

        if print_log:
            print(msg)

        Logges.write_logs(msg=msg)

    @staticmethod
    def to_markdown() -> None:
        """Convert days logs as markdown file.."""
        icons = {"INFO": ":passport_control:", "WARNING": ":vs:", "ERROR": ":sos:"}
        type_counter = [0, 0, 0]
        md_file = os.path.join(
            SAVINGPATH,
            get_daily_log_file_name(filename=Logges.get_log_name(), markdown=True),
        )
        markdown_file = open(md_file, "w")

        filename = get_daily_log_file_name(filename=Logges.get_log_name())
        file_dir = get_saving_path()
        log_path = os.path.join(file_dir, filename)
        with open(log_path, "r") as file:
            logs = file.readlines()
            file.close()
        only_filename = "_".join(filename.split("_")[1:]) + ".py".replace(".log", "")
        file_date = filename.split("_")[0]

        if get_current_platform_name() == "Windows":
            only_filename = os.path.split(only_filename)[1]
        markdown_file.writelines(
            f"# {only_filename} {file_date} Logs :see_no_evil: :hear_no_evil: :speak_no_evil:\n"
        )
        markdown_file.writelines("![](pie_chart.png)\n")
        markdown_file.writelines("|TYPE|TIME|MESSAGE|\n| :--: | :--: | :--: |\n")
        for each_log in logs[::-1]:
            log_type = (
                each_log.split("\t")[0].split(" ")[0].replace("[", "").replace("]", "")
            )
            if log_type == list(icons.keys())[0]:
                type_counter[0] += 1
            elif log_type == list(icons.keys())[1]:
                type_counter[1] += 1
            elif log_type == list(icons.keys())[2]:
                type_counter[2] += 1

            log_time = (
                each_log.split("\t")[0]
                .split(" ")[1]
                .replace("[", "")
                .replace("]", "")[0:-1]
            )
            log_msg = each_log.split("\t")[1]
            log_msg.replace("\n", "")
            try:
                markdown_file.writelines(
                    f"|{icons[log_type]} | {log_time} | {log_msg.strip()}| "
                )
                markdown_file.writelines("\n")
            except:
                raise ("Please check your icon.")
        markdown_file.writelines(
            "All right reserved 2022 &copy;&nbsp; [Logges](https://github.com/uysalserkan/Logges) - *[uysalserkan](https://github.com/uysalserkan/) & [Ozkan](https://github.com/ozkanuysal)*\n"
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
        console_data(script_name=Logges.get_log_name())

    @staticmethod
    def to_pdf() -> None:
        """Convert logs to pdf file with day logs."""
        to_pdf(script_name=Logges.get_log_name(), saving_path=SAVINGPATH)
