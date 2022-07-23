"""An ultimate logger for python.

@author: Serkan UYSAL
@email: uysalserkan08@gmail.com
"""

import os
from .utils import (create_pie_chart, console_data, get_saving_path, get_current_time_HM, get_daily_log_file_name, to_pdf, get_current_platform_name)

STATUS = ["INFO", "WARNING", "ERROR"]
FILENAME = None
SAVINGPATH = None


class Logges:
    """TODO: Buraya standartlara uygun bir açıklama eklenecek."""

    @staticmethod
    def setup(filepath) -> None:
        """You need to enter just `__file__` input to filepath arguemnt."""
        global FILENAME, SAVINGPATH
        path = os.path.abspath(filepath)
        FILENAME = os.path.split(path)[1].split(".py")[0]
        SAVINGPATH = os.path.split(path)[0]

    @staticmethod
    def write_logs(msg: str):
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        filename = get_daily_log_file_name(filename=Logges.get_log_name())
        saving_dir = get_saving_path()
        log_dir = os.path.join(saving_dir, filename)
        log_file = open(f"{log_dir}", 'a')
        log_file.writelines(msg + "\n")

    def get_status_message(status: int) -> str:
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        status_text = f"[{STATUS[status]}] "
        return status_text

    @staticmethod
    def get_log_name() -> str:
        """TODO: Buraya standartlara uygun açıklama gelecek."""
        global FILENAME
        return FILENAME

    @staticmethod
    def log(log: str, status: int = 0, print_log: bool = True):
        """TODO: Buraya standartlara uygun açıklama gelecek."""
        cur_time = get_current_time_HM()
        status = Logges.get_status_message(status=status)
        msg = f"{status}{cur_time}\t{log}"

        if print_log:
            print(msg)

        Logges.write_logs(msg=msg)

    @staticmethod
    def to_markdown():
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        icons = {
            "INFO": ":passport_control:",
            "WARNING": ":vs:",
            "ERROR": ":sos:"
        }
        type_counter = [0, 0, 0]
        md_file = os.path.join(SAVINGPATH, get_daily_log_file_name(filename=Logges.get_log_name(), markdown=True))
        markdown_file = open(md_file, 'w')

        filename = get_daily_log_file_name(filename=Logges.get_log_name())
        file_dir = get_saving_path()
        log_path = os.path.join(file_dir, filename)
        with open(log_path, 'r') as file:
            logs = file.readlines()
            file.close()
        only_filename = "_".join(filename.split('_')[1:]) + ".py".replace(".log", '')
        file_date = filename.split('_')[0]

        if get_current_platform_name() == "Windows":
            only_filename = os.path.split(only_filename)[1]
        markdown_file.writelines(f"# {only_filename} {file_date} Logs :see_no_evil: :hear_no_evil: :speak_no_evil:\n")
        markdown_file.writelines("![](pie_chart.png)\n")
        markdown_file.writelines("|TYPE|TIME|MESSAGE|\n| :--: | :--: | :--: |\n")
        for each_log in logs[::-1]:
            log_type = each_log.split("\t")[0].split(" ")[0].replace('[', '').replace(']', '')
            if log_type == list(icons.keys())[0]:
                type_counter[0] += 1
            elif log_type == list(icons.keys())[1]:
                type_counter[1] += 1
            elif log_type == list(icons.keys())[2]:
                type_counter[2] += 1

            log_time = each_log.split("\t")[0].split(" ")[1].replace('[', '').replace(']', '')[0:-1]
            log_msg = each_log.split("\t")[1]
            log_msg.replace("\n", '')
            try:
                markdown_file.writelines(f"|{icons[log_type]} | {log_time} | {log_msg.strip()}| ")
                markdown_file.writelines("\n")
            except:
                raise("Please check your icon.")
        markdown_file.writelines("All right reserved 2022 &copy;&nbsp; [Logges](https://github.com/uysalserkan/Logges) - *[uysalserkan](https://github.com/uysalserkan/) & [Ozkan](https://github.com/ozkanuysal)*\n")
        create_pie_chart(saving_path=SAVINGPATH, info_size=type_counter[0], warning_size=type_counter[1], error_size=type_counter[2])

    @staticmethod
    def console_data():
        """We are printing our data on console."""
        console_data(script_name=Logges.get_log_name())

    @staticmethod
    def to_pdf():
        """We create a pdf file about logs and charts."""
        to_pdf(script_name=Logges.get_log_name(), saving_path=SAVINGPATH)
