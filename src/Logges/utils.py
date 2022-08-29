"""There are some functions used in logges.

@package: Logges
@authors: Serkan UYSAL, Özkan UYSAL
@date: 2022
@mails: uysalserkan08@gmail.com, ozkan.uysal.2009@hotmail.com
"""
import datetime
import os
import platform
import sys
from typing import Tuple

import matplotlib.pyplot as plt
from reportlab.lib.colors import Color
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import inch
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Image
from reportlab.platypus import PageBreak
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table as reportlabTable
from reportlab.platypus import TableStyle
from rich.console import Console
from rich.table import Table


def get_current_platform_name() -> str:
    """get_current_platform_name method return current platform name like Windows, Linux, OSX.

    Return:
        sys_name `string`: System platform name.
    """
    sys_name = platform.system()
    return sys_name


def get_saving_path(log_dir: bool = False) -> str:
    """get_saving_path method save the hidden log files to package directory.

    Parameters:
        log_dir `bool`: If you want to store all logs to logs directory, set True, default is False.

    Return:
        dir_path `str`:  Name of saving path which will contain all log files.
    """
    script_path = os.path.realpath(__file__)
    dir_path = os.path.split(script_path)[0]
    if log_dir:
        dir_path += os.path.join(dir_path, "logs")
    return dir_path


def create_pie_chart(saving_path: str,
                     info_size: int = 0,
                     warning_size: int = 0,
                     error_size: int = 0) -> None:
    """We are creating and saving a plot that show us the rate of log types.

    Parameters:
        saving_path `str`: pic_chart.png saved on that parameter as path.
        info_size `int`: Info logs length.
        warning_size `int`: Warning logs length.
        error_size `int`: Error logs lenght.

    Return:
        None
    """
    chart_labels = ["INFO", "WARNING", "ERROR"]
    chart_explode = [0, 0.01, 0.01]
    chart_colors = ["blue", "yellow", "red"]

    logs_size = [info_size, warning_size, error_size]

    plt.pie(
        logs_size,
        labels=chart_labels,
        explode=chart_explode,
        colors=chart_colors,
        autopct="%1.1f%%",
    )

    png_path = os.path.join(saving_path, "pie_chart.png")

    plt.savefig(f"{png_path}")


def get_daily_log_file_name(filename: str,
                            markdown: bool = False,
                            pdf: bool = False) -> str:
    """get_daily_log_file_name.

    get_daily_log_file_name method returns a filename, which will be name of the saving file,
    priority sequence is: pdf, markdown and log file.

    Parameters:
        filename `str`: Running script name.
        markdown `bool`: If you want to save your logs as markdwon file, set that parameter to True, default is False.
        pdf `bool`: If you want to save your logs as pdf file, set that parameter to True, default is False.

    Return:
        filename `str`: Full name of file name with specific extension.
    """
    if pdf:
        filename = f"{datetime.datetime.today().strftime('%Y-%m-%d')}_{filename}.pdf"
    elif markdown:
        filename = f"{datetime.datetime.today().strftime('%Y-%m-%d')}_{filename}.md"
    else:
        filename = f"{datetime.datetime.today().strftime('%Y-%m-%d')}_{filename}.log"
    return filename


def get_current_time_HM() -> str:
    """We need that information for log with current time.

    Return:
        hour_min_sec `str`: Current hour:minute:second.
    """
    hour_min_sec = datetime.datetime.today().strftime("%H:%M:%S")
    return f"{hour_min_sec}"


def console_data(script_name: str) -> None:
    """We are printing our logs on console with beauty of rich.

    Params:
        script_name (str): That contains the script name which is running on console.

    Return:
        None
    """
    dir_path = get_saving_path()

    log_dir = os.path.join(dir_path,
                           get_daily_log_file_name(filename=script_name))
    filename = f"{log_dir}"

    rich_table = Table(
        title=
        f"{filename.split('/')[-1]} :see_no_evil: :hear_no_evil: :speak_no_evil:"
    )

    rich_table.add_column("Type", justify="left", style="white", no_wrap=True)
    rich_table.add_column("Message", justify="left", style="magenta")
    rich_table.add_column("Log Date", justify="center", style="green")

    icons = {"INFO": ":passport_control:", "WARNING": ":vs:", "ERROR": ":sos:"}

    with open(f"{filename}", "r") as file:
        logs = file.readlines()
        file.close()

    type_counter = [0, 0, 0]
    for each_log in logs[::-1]:
        color = ""
        log_type = (each_log.split("\t")[0].split(" ")[0].replace("[",
                                                                  "").replace(
                                                                      "]", ""))
        if log_type == list(icons.keys())[0]:
            color = "cyan"
            type_counter[0] += 1
        elif log_type == list(icons.keys())[1]:
            color = "yellow"
            type_counter[1] += 1
        elif log_type == list(icons.keys())[2]:
            color = "red"
            type_counter[2] += 1

        log_time = (each_log.split("\t")[0].split(" ")[1].replace(
            "[", "").replace("]", "")[0:-1])
        log_msg = each_log.split("\t")[1]
        log_msg.replace("\n", "")
        try:
            rich_table.add_row(
                f"[bold]{icons[log_type]} {log_type}",
                f"[{color}]{log_msg}",
                f"[italic]{log_time}",
            )
        except KeyError:
            raise ("Please check your icon.")
    rich_console = Console()
    rich_console.print(rich_table)
    total_length = type_counter[0] + type_counter[1] + type_counter[2]
    rich_console.print(
        "[blue]████████████████[yellow]████████████████[red]██████████████████"
    )
    rich_console.print(
        f"Info: %{round(type_counter[0]/total_length*100, 2)}\tWarning: %{round(type_counter[1]/total_length*100, 2)}\
\tError: %{round(type_counter[2]/total_length*100, 2)}")


def to_pdf(script_name: str, saving_path: str) -> None:
    """Export the logs to a file with `.pdf` format.

    Parameters:
        script_name `str`: Save the pdf file as that string.
        saving_path `str`:  Save the pdf file to the that path.

    Return:
        None
    """

    def copyright_text() -> Paragraph:
        """We are add a text on the page."""
        uysaltext = 'All right reserved 2022 &copy;&nbsp;<a href="https://github.com/uysalserkan/Logges">Logges</a> - \
<strong><a href="https://github.com/uysalserkan">uysalserkan</a></strong> & \
<strong><a href="https://github.com/ozkanuysal">Ozkan</a></strong>'

        copyright_style = ParagraphStyle("copyright_style",
                                         fontSize=8,
                                         alignment=TA_CENTER)
        uysaltext_p = Paragraph(uysaltext, copyright_style)
        return uysaltext_p

    type_colors = {"INFO": "blue", "WARNING": "orange", "ERROR": "red"}
    dir_path = get_saving_path()

    log_dir = os.path.join(dir_path,
                           get_daily_log_file_name(filename=script_name))
    filename = f"{log_dir}"

    # Burada eklemeler yapılıyor..
    page_elements = []

    # Reading data başlıyor..
    with open(f"{filename}", "r") as file:
        logs = file.readlines()
        file.close()

    # Header Başlığı Ekleniyor.
    header_text = (
        f"{script_name}.py {datetime.datetime.today().strftime('%Y-%m-%d')} Logs"
    )
    header_style = ParagraphStyle("H1", fontSize=18, alignment=TA_LEFT)
    header = Paragraph(header_text, header_style)
    page_elements.append(header)
    page_elements.append(Spacer(10, 20))

    if not os.path.exists(f"{saving_path}/pie_chart.png"):
        info_, warn_, err_ = (0, 0, 0)
        for each_log in logs[::-1]:
            log_type = (each_log.split("\t")[0].split(" ")[0].replace(
                "[", "").replace("]", ""))
            if log_type == list(type_colors.keys())[0]:
                info_ += 1
            elif log_type == list(type_colors.keys())[1]:
                warn_ += 1
            elif log_type == list(type_colors.keys())[2]:
                err_ += 1
        create_pie_chart(
            saving_path=saving_path,
            info_size=info_,
            warning_size=warn_,
            error_size=err_,
        )
    png_path = os.path.join(saving_path, "pie_chart.png")
    img = Image(f"{png_path}")
    img.drawHeight = 3.5 * inch
    img.drawWidth = 5.5 * inch
    page_elements.append(img)

    table_data = []

    column_styled_list = []
    centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
    columns = ["Status", "Time", "Message"]

    for each in columns:
        column_text = f"<font size='12'><b>{each}</b></font>"
        styled_column = Paragraph(column_text, centered)
        column_styled_list.append(styled_column)
    table_data.append(column_styled_list)

    alignStyle = ParagraphStyle(name="data", alignment=TA_CENTER)

    # Reading data bitiyor..
    for each_log in logs[::-1]:
        log_type = (each_log.split("\t")[0].split(" ")[0].replace("[",
                                                                  "").replace(
                                                                      "]", ""))
        log_time = (each_log.split("\t")[0].split(" ")[1].replace(
            "[", "").replace("]", "")[0:-1])
        log_msg = each_log.split("\t")[1]
        log_msg.replace("\n", "")

        color = type_colors[log_type]

        each_row = []
        for index, each_item in enumerate([log_type, log_time, log_msg]):
            if index == 2:
                table_text = f"<font color='{color}'>{each_item}</font>"
            else:
                table_text = f"<b>{each_item}</b>"
            ptext = Paragraph(table_text, alignStyle)
            each_row.append(ptext)
        table_data.append(each_row)

    table = reportlabTable(table_data, colWidths=[70, 70, 350])
    tStyle = TableStyle([
        ("ALIGN", (0, -1), (-1, -1), "LEFT"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("LINEABOVE", (0, 0), (-1, -1), 1, Color(0.2, 0.3, 0.4)),
        ("BACKGROUND", (0, 0), (-1, 0), Color(102 / 255, 191 / 255,
                                              191 / 255)),
    ])
    table.setStyle(tStyle)
    page_elements.append(table)

    page_elements.append(copyright_text())
    page_elements.append(PageBreak())
    to_pdf_path = os.path.join(
        saving_path, get_daily_log_file_name(filename=script_name, pdf=True))
    pdf_doc = SimpleDocTemplate(to_pdf_path, pagesize=LETTER)
    pdf_doc.multiBuild(page_elements)


def get_log_info() -> Tuple[str, str]:
    """We are getting calling file path and function name:line nuber."""
    frame = sys._getframe().f_back.f_back
    filepath = frame.f_code.co_filename
    funct_name = frame.f_code.co_name
    line_num = frame.f_lineno
    return (filepath, f"{funct_name}:{line_num}")
