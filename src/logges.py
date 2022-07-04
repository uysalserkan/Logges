"""An ultimate logger for python.

@author: Serkan UYSAL
@email: uysalserkan08@gmail.com
"""

import os
import temp
from utils import create_pie_chart
from utils import console_data
from utils import get_saving_path
from utils import get_current_time_HM
from utils import get_daily_log_file_name


STATUS = ["INFO", "WARNING", "ERROR"]


class Logges:
    """TODO: Buraya standartlara uygun bir açıklama eklenecek."""

    @staticmethod
    def write_logs(msg):
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        filename = get_daily_log_file_name(filename=Logges.get_log_name())
        saving_dir = get_saving_path()
        log_file = open(f"{saving_dir}/{filename}", 'a')
        log_file.writelines(msg + "\n")
        # log_file.write("\n")

    def get_status_message(status: int) -> str:
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        status_text = f"[{STATUS[status]}] "
        return status_text

    @staticmethod
    def get_log_name() -> str:
        """TODO: Buraya standartlara uygun açıklama gelecek."""
        return os.path.basename(__file__).split('.py')[0]

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
        md_file = get_saving_path() + '/' + get_daily_log_file_name(filename=Logges.get_log_name(), markdown=True)
        markdown_file = open(md_file, 'w')

        filename = get_daily_log_file_name(filename=Logges.get_log_name())
        file_dir = get_saving_path()
        with open(f"{file_dir}/{filename}", 'r') as file:
            logs = file.readlines()
            file.close()
        only_filename = filename.split('_')[0] + ".py"
        file_date = filename.split('_')[1].replace(".log", '')

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
        create_pie_chart(info_size=type_counter[0], warning_size=type_counter[1], error_size=type_counter[2])

    @staticmethod
    def to_console():
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        pass

    @staticmethod
    def to_pdf():
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        pass


if __name__ == '__main__':
    Logges.log("It is a not INFO log.", 2, print_log=False)
    # Logges.log("It is a not ERROR log.", 1)
    temp.temp_func()
    Logges.to_markdown()
    console_data(script_name=Logges.get_log_name())
