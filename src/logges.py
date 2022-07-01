"""An ultimate logger for python.

@author: Serkan UYSAL
@email: uysalserkan08@gmail.com
"""

import os
import datetime
import temp


STATUS = ["INFO", "WARNING", "ERROR"]


class Logges:
    """TODO: Buraya standartlara uygun bir açıklama eklenecek."""

    @staticmethod
    def write_logs(msg):
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        filename = Logges.get_daily_log_file_name()
        saving_dir = Logges.get_saving_path()
        log_file = open(f"{saving_dir}/{filename}", 'a')
        log_file.writelines(msg + "\n")
        # log_file.write("\n")

    def get_status_message(status: int) -> str:
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        status_text = f"[{STATUS[status]}] "
        return status_text

    def get_daily_log_file_name(markdown: bool = False, pdf: bool = False) -> str:
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        if pdf:
            filename = f"{os.path.basename(__file__).split('.py')[0]}_{datetime.datetime.today().strftime('%Y-%m-%d')}.pdf"
        elif markdown:
            filename = f"{os.path.basename(__file__).split('.py')[0]}_{datetime.datetime.today().strftime('%Y-%m-%d')}.md"
        else:
            filename = f"{os.path.basename(__file__).split('.py')[0]}_{datetime.datetime.today().strftime('%Y-%m-%d')}.log"
        return filename

    def get_current_time_HM():
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        hour_min_sec = datetime.datetime.today().strftime('%H:%M:%S')
        return f"[{hour_min_sec}]: "

    @staticmethod
    def set_logger_name(log_name: str):
        """TODO: Buraya standartlara uygun açıklama gelecek."""
        pass

    @staticmethod
    def log(log: str, status: int = 0, print_log: bool = True):
        """TODO: Buraya standartlara uygun açıklama gelecek."""
        cur_time = Logges.get_current_time_HM()
        status = Logges.get_status_message(status=status)
        msg = f"{status}{cur_time}\t{log}"

        if print_log:
            print(msg)

        Logges.write_logs(msg=msg)

    def get_saving_path(log_dir: bool = False):
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        script_path = os.path.realpath(__file__)
        dir_path = "/".join(script_path.split('/')[:-1])

        if log_dir:
            dir_path += "/logs"
        return dir_path

    @staticmethod
    def to_markdown():
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        icons = {
            "INFO": ":passport_control:",
            "WARNING": ":vs:",
            "ERROR": ":sos:"
        }
        md_file = Logges.get_saving_path() + '/' + Logges.get_daily_log_file_name(markdown=True)
        markdown_file = open(md_file, 'w')

        filename = Logges.get_daily_log_file_name()
        file_dir = Logges.get_saving_path()
        with open(f"{file_dir}/{filename}", 'r') as file:
            logs = file.readlines()
            file.close()
        only_filename = filename.split('_')[0] + ".py"
        file_date = filename.split('_')[1].replace(".log", '')

        markdown_file.writelines(f"# {only_filename} {file_date} Logs :see_no_evil: :hear_no_evil: :speak_no_evil:\n")
        markdown_file.writelines("|TYPE|TIME|MESSAGE|\n| :--: | :--: | :--: |\n")
        for each_log in logs[::-1]:
            log_type = each_log.split("\t")[0].split(" ")[0].replace('[', '').replace(']', '')
            log_time = each_log.split("\t")[0].split(" ")[1].replace('[', '').replace(']', '')[0:-1]
            log_msg = each_log.split("\t")[1]
            log_msg.replace("\n", '')
            try:
                markdown_file.writelines(f"|{icons[log_type]} | {log_time} | {log_msg.strip()}| ")
                markdown_file.writelines("\n")
            except:
                raise("Please check your icon.")

    @staticmethod
    def to_console():
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        pass

    @staticmethod
    def to_pdf():
        """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
        pass


if __name__ == '__main__':
    Logges.log("It is a not INFO log.", 2)
    Logges.to_markdown()
    temp.temp_func()
    Logges.to_markdown()
