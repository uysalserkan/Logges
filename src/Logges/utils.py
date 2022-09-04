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
from io import TextIOWrapper
from typing import Dict
from typing import List
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


def create_pie_chart(saving_path: str, status_dict: Dict[str, int]) -> None:
    """We are creating and saving a plot that show us the rate of log types.

    Parameters:
        saving_path `str`: pic_chart.png saved on that parameter as path.
        info_size `int`: Info logs length.
        warning_size `int`: Warning logs length.
        error_size `int`: Error logs lenght.

    Return:
        None
    """
    chart_labels = list(status_dict.keys())
    chart_explode = [0, 0.01, 0.01, 0.01, 0.01]
    chart_colors = ["gray", "blue", "yellow", "red", "darkred"]

    logs_size = list(status_dict.values())

    plt.pie(
        logs_size,
        labels=chart_labels,
        explode=chart_explode,
        colors=chart_colors,
        autopct="%1.1f%%",
    )

    png_path = os.path.join(saving_path, "pie_chart.png")

    if os.path.exists("pie_chart.png"):
        os.remove(png_path)

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


def console_data(
    script_name: str,
    status_dict: Dict[str, int],
    statuc_icon_dict: Dict[str, str],
    local_file: bool,
) -> None:
    """We are printing our logs on console with beauty of rich.

    Params:
        script_name (str): That contains the script name which is running on console.
        stats_dict `Dict`:  Define status counter.

    Return:
        None
    """
    if local_file:
        log_dir = script_name
    else:
        dir_path = get_saving_path()
        log_dir = os.path.join(dir_path, script_name)

    file = open(log_dir, "r")

    (
        _date_list,
        _status_list,
        _filename_list,
        _functname_list,
        _log_message_list,
    ) = extract_logs(logs=file)

    type_colors = {
        "DEBUG": "[bright_black]",
        "INFO": "[blue]",
        "WARNING": "[bright_yellow]",
        "ERROR": "[red]",
        "CRITICAL": "[bold red]",
    }

    rich_table = Table(
        title=
        f"{log_dir.split('/')[-1]} :see_no_evil: :hear_no_evil: :speak_no_evil:"
    )

    rich_table.add_column("DATE", justify="center")
    rich_table.add_column("STATUS", justify="center", no_wrap=True)
    rich_table.add_column("FILE", justify="center")
    rich_table.add_column("FUNCTION", justify="center")
    rich_table.add_column("MESSAGE",
                          justify="left",
                          no_wrap=False,
                          max_width=250)

    for index, _ in enumerate(_log_message_list):
        log_status_clear = _status_list[index].replace("[",
                                                       "").replace("]", "")
        status_dict[log_status_clear] += 1
        rich_table.add_row(
            f"[bold]{_date_list[index]}",
            f"{type_colors[log_status_clear]}[{log_status_clear} {statuc_icon_dict[log_status_clear]}][white]",
            f"[bold]{_filename_list[index].replace('[', '').replace(']', '')}",
            f"[italic]{_functname_list[index].replace('[', '').replace(']', '')}",
            f"{_log_message_list[index]}",
        )

    rich_console = Console()
    rich_console.print(rich_table)
    total_length = sum(list(status_dict.values()))
    rich_console.print("[bright_black]████████████████[blue]████████████████\
[bright_yellow]████████████████[red]█████████████████[dark_red]██████████████████"
                       )
    rich_console.print(
        f"DEBUG: %{round(status_dict['DEBUG']/total_length*100 if total_length > 0 else 0, 2)}"
        +
        f"\tINFO: %{round(status_dict['INFO']/total_length*100 if total_length > 0 else 0, 2)}"
        +
        f"\tWARNING: %{round(status_dict['WARNING']/total_length*100 if total_length > 0 else 0, 2)}"
        +
        f"\tERROR: %{round(status_dict['ERROR']/total_length*100 if total_length > 0 else 0, 2)}"
        +
        f"\tCRITICAL: %{round(status_dict['CRITICAL']/total_length*100 if total_length > 0 else 0, 2)}"
    )


def to_markdown(
    script_name: str,
    saving_path: str,
    status_dict: Dict[str, int],
    status_icons: Dict[str, str],
    local_file: bool = False,
) -> None:
    """Export the logs to a file with `.pdf` format.

    Parameters:
        script_name `str`: Save the pdf file as that string.
        saving_path `str`:  Save the pdf file to the that path.
        stats_dict `Dict`:  Define status counter.
        local_file: `bool`: Check load from root directory or local file. Default is False.

    Return:
        None
    """
    if local_file:
        md_file = os.path.join(saving_path, script_name.replace(".log", ".md"))

        markdown_file = open(md_file, "w")
        filename = script_name

    else:
        md_file = os.path.join(
            saving_path,
            get_daily_log_file_name(filename=script_name, markdown=True))

        markdown_file = open(md_file, "w")
        filename = get_daily_log_file_name(filename=script_name)

    file_dir = saving_path
    full_logfile_path = os.path.join(file_dir, filename)

    only_filename = "_".join(filename.split("_")[1:]) + ".py".replace(
        ".log", "")
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

    # Write logs in markdown file.
    for index, _ in enumerate(_log_message_list):
        log_status_clear = _status_list[index].replace("[",
                                                       "").replace("]", "")
        status_dict[log_status_clear] += 1

        try:
            markdown_file.writelines("|{}|{}|{}|{}|{}|".format(
                _date_list[index],
                status_icons[log_status_clear],
                _filename_list[index],
                _functname_list[index],
                _log_message_list[index].replace("\n", " "),
            ))
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
        saving_path=saving_path,
        status_dict=status_dict,
    )

    markdown_file.close()


def to_pdf(
    script_name: str,
    saving_path: str,
    status_dict: Dict[str, int],
    local_file: bool = False,
) -> None:
    """Export the logs to a file with `.pdf` format.

    Parameters:
        script_name `str`: Save the pdf file as that string.
        saving_path `str`:  Save the pdf file to the that path.
        stats_dict `Dict`:  Define status counter.
        local_file: `bool`: Check load from root directory or local file. Default is False.

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

    type_colors = {
        "DEBUG": "gray",
        "INFO": "blue",
        "WARNING": "orange",
        "ERROR": "red",
        "CRITICAL": "darkred",
    }

    if local_file:
        log_dir = script_name
    else:

        log_dir = os.path.join(saving_path,
                               get_daily_log_file_name(filename=script_name))

    # Burada eklemeler yapılıyor..
    page_elements = []

    # Reading data başlıyor..
    file = open(log_dir, "r")

    (
        _date_list,
        _status_list,
        _filename_list,
        _functname_list,
        _log_message_list,
    ) = extract_logs(logs=file)

    # Header Başlığı Ekleniyor.
    header_text = (
        f"{script_name}.py {datetime.datetime.today().strftime('%Y-%m-%d')} Logs"
    )
    header_style = ParagraphStyle("H1", fontSize=18, alignment=TA_LEFT)
    header = Paragraph(header_text, header_style)
    page_elements.append(header)
    page_elements.append(Spacer(10, 20))

    if not os.path.exists(os.path.join(saving_path, "pie_chart.png")):
        for index, _ in enumerate(_status_list):
            log_status_clear = _status_list[index].replace("[", "").replace(
                "]", "")
            status_dict[log_status_clear] += 1

        create_pie_chart(
            saving_path=saving_path,
            status_dict=status_dict,
        )

    # Append image to PDF file.
    png_path = os.path.join(saving_path, "pie_chart.png")
    img = Image(f"{png_path}")
    img.drawHeight = 3.5 * inch
    img.drawWidth = 5.5 * inch
    page_elements.append(img)

    table_data = []

    column_styled_list = []
    centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
    columns = ["TIME", "STATUS", "FILE", "FUNCTION", "MESSAGE"]

    for each in columns:
        column_text = f"<font size='8'><b>{each}</b></font>"
        styled_column = Paragraph(column_text, centered)
        column_styled_list.append(styled_column)
    table_data.append(column_styled_list)

    alignStyle = ParagraphStyle(name="data", alignment=TA_CENTER)

    # Reading data bitiyor..

    # Write logs into pdf.
    for index, _ in enumerate(_log_message_list):
        # Log message color
        log_status_clear = _status_list[index].replace("[",
                                                       "").replace("]", "")
        color = type_colors[log_status_clear]

        # Extract values of log data.
        _date = _date_list[index]
        _log_status = log_status_clear
        _filename = _filename_list[index]
        _functname = _functname_list[index]
        _log_msg = _log_message_list[index]

        row_data = []
        for index, item in enumerate(
            [_date, _log_status, _filename, _functname, _log_msg]):
            if index == 1:
                table_text = f"<font color='{color}'>{item}</font>"
            else:
                table_text = f"<b>{item}</b>"
            ptext = Paragraph(table_text, alignStyle)
            row_data.append(ptext)
        table_data.append(row_data)

    table = reportlabTable(table_data, colWidths=[70, 100, 100, 100, 200])
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


def extract_logs(
    logs: TextIOWrapper,
) -> Tuple[List[str], List[str], List[str], List[str], List[str]]:
    """Extract logs meta-data and messages.

    Parameters:
        logs `TextIOWrapper`: An object that comes with open method.

    Return:
        Tuple `List of str`: Meta-data and messages.

        `(date_list, status_list, filename_list, function_and_lineno_list, msg_list)`
    """
    date_list = []
    status_list = []
    filename_list = []
    function_and_lineno_list = []
    msg_list = []
    for each_line in logs.readlines():
        if not each_line.startswith("[") and len(msg_list) <= 0:
            continue
        elif each_line.startswith("["):
            # Get Meta-Data
            info_str = ":".join(each_line.split(":")[:4]).strip()
            msg_str = ":".join(each_line.split(":")[4:])

            # Append Log message
            msg_list.append(msg_str)

            # Extract Infos
            date_list.append(info_str[0:10])
            status_list.append(info_str[11:21].replace(" ", ""))
            filename_list.append(f"[{info_str[22:].split('[')[1][:-2]}]")
            function_and_lineno_list.append(
                f"[{info_str[22:].split('[')[2][:-1]}]")
        else:
            msg_list[len(msg_list) - 1] += each_line

    return (date_list, status_list, filename_list, function_and_lineno_list,
            msg_list)
