"""There are some functions used in logges."""

import os
import datetime
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table


def get_saving_path(log_dir: bool = False):
    """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
    script_path = os.path.realpath(__file__)
    dir_path = "/".join(script_path.split('/')[:-1])

    if log_dir:
        dir_path += "/logs"
    return dir_path


def create_pie_chart(info_size: bool = 0, warning_size: bool = 0, error_size: bool = 0) -> None:
    """We are creating and saving a plot that show us the rate of log types."""
    chart_labels = ["INFO", "WARNING", "ERROR"]
    chart_explode = [0, 0.01, 0.01]
    chart_colors = ['blue', 'yellow', 'red']

    logs_size = [info_size, warning_size, error_size]

    plt.pie(logs_size, labels=chart_labels, explode=chart_explode, colors=chart_colors, autopct='%1.1f%%')

    script_path = os.path.realpath(__file__)
    dir_path = "/".join(script_path.split('/')[:-1])

    plt.savefig(f"{dir_path}/pie_chart.png")


def get_daily_log_file_name(filename: str, markdown: bool = False, pdf: bool = False) -> str:
    """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
    if pdf:
        filename = f"{filename}_{datetime.datetime.today().strftime('%Y-%m-%d')}.pdf"
    elif markdown:
        filename = f"{filename}_{datetime.datetime.today().strftime('%Y-%m-%d')}.md"
    else:
        filename = f"{filename}_{datetime.datetime.today().strftime('%Y-%m-%d')}.log"
    return filename


def get_current_time_HM():
    """TODO: Buraya standartlara uygun bir açıklama eklenecek."""
    hour_min_sec = datetime.datetime.today().strftime('%H:%M:%S')
    return f"[{hour_min_sec}]: "


def console_data(script_name: str) -> None:
    """We are printing our logs on console with beauty of rich."""
    dir_path = get_saving_path()

    filename = f"{dir_path}/{script_name}_{datetime.datetime.today().strftime('%Y-%m-%d')}.log"

    rich_table = Table(title=f"{filename.split('/')[-1]} :see_no_evil: :hear_no_evil: :speak_no_evil:")

    rich_table.add_column("Type", justify="left", style="white", no_wrap=True)
    rich_table.add_column("Message", justify="left", style="magenta")
    rich_table.add_column("Log Date", justify="center", style="green")

    icons = {
        "INFO": ":passport_control:",
        "WARNING": ":vs:",
        "ERROR": ":sos:"
    }

    with open(f"{filename}", 'r') as file:
        logs = file.readlines()
        file.close()

    type_counter = [0, 0, 0]
    for each_log in logs[::-1]:
        color = ""
        log_type = each_log.split("\t")[0].split(" ")[0].replace('[', '').replace(']', '')
        if log_type == list(icons.keys())[0]:
            color = "cyan"
            type_counter[0] += 1
        elif log_type == list(icons.keys())[1]:
            color = "yellow"
            type_counter[1] += 1
        elif log_type == list(icons.keys())[2]:
            color = "red"
            type_counter[2] += 1

        log_time = each_log.split("\t")[0].split(" ")[1].replace('[', '').replace(']', '')[0:-1]
        log_msg = each_log.split("\t")[1]
        log_msg.replace("\n", '')
        try:
            rich_table.add_row(f"[bold]{icons[log_type]} {log_type}", f"[{color}]{log_msg}", f"[italic]{log_time}")
        except:
            raise("Please check your icon.")
    rich_console = Console()
    rich_console.print(rich_table)
    total_length = type_counter[0] + type_counter[1] + type_counter[2]
    rich_console.print("[blue]████████████████[yellow]████████████████[red]██████████████████")
    rich_console.print(f"Info: %{round(type_counter[0]/total_length*100, 2)}\tWarning: %{round(type_counter[1]/total_length*100, 2)}\tError: %{round(type_counter[2]/total_length*100, 2)}")
