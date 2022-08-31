"""CLI app."""
import os
from typing import Union

import click
from Logges import Logges

from .utils import extract_logs
from .utils import console_data


def validate_file(_, __, value):
    """VALIDATE."""
    log_files = []
    for each_file in os.listdir(os.path.split(__file__)[0]):
        if ".log" in each_file:
            log_files.append(each_file)
    if value not in log_files:
        raise click.BadParameter(
            message="Please enter a " +
            click.style("valid", fg="red", reverse=True, underline=True) +
            " log filename.")
    else:
        return value


def validate_date(_, __, value):
    """VALIDATE."""
    if isinstance(value, type(None)):
        return value

    elif len(str(value)) < 8:
        raise click.BadParameter(
            message="Please enter date format as: " +
            click.style("1998-08-25", fg="red", blink=True))

    if value[4] == ":" and value[7] == ":":
        return str(value).replace(":", "-")

    elif value[4] == "-" and value[7] == "-":
        return str(value)

    elif len(str(value)) == 8:
        date_str = str(value)
        return date_str[:4] + "-" + date_str[4:6] + "-" + date_str[6:]

    else:
        raise click.BadParameter(
            message="Please enter date format as: " +
            click.style("1998-08-25", fg="red", blink=True))


@click.group(name="Logges-cli")
@click.version_option(version="2.0", package_name="Logges", prog_name="Logges")
def Logges_cli():
    """ALL Base of group of options."""
    pass


@Logges_cli.command(name="list", help="List all log files.")
@click.option(
    "--max_date",
    required=False,
    help="Show logs of maximum date.",
    callback=validate_date,
)
@click.option(
    "--min_date",
    required=False,
    help="Show logs of minimum date.",
    callback=validate_date,
)
def list_logs(max_date: str, min_date: str):
    """LIST."""
    log_file_list = []
    for each_file in os.listdir(os.path.split(__file__)[0]):
        if ".log" in each_file:
            if (not isinstance(min_date, type(None))) and (not isinstance(
                    max_date, type(None))):
                if (each_file[:10] >= min_date) and (each_file[:10] <=
                                                     max_date):
                    log_file_list.append(
                        click.style(text="*: ", fg="bright_green", bold=True) +
                        click.style(
                            text=each_file, fg="bright_cyan", italic=True))
            elif not isinstance(min_date, type(None)):
                if each_file[:10] >= min_date:
                    log_file_list.append(
                        click.style(text="*: ", fg="bright_green", bold=True) +
                        click.style(
                            text=each_file, fg="bright_cyan", italic=True))
            elif not isinstance(max_date, type(None)):
                if each_file[:10] <= max_date:
                    log_file_list.append(
                        click.style(text="*: ", fg="bright_green", bold=True) +
                        click.style(
                            text=each_file, fg="bright_cyan", italic=True))
            else:
                log_file_list.append(
                    click.style(text="*: ", fg="bright_green", bold=True) +
                    click.style(text=each_file, fg="bright_cyan", italic=True))
    click.echo_via_pager("\n".join(log_file_list))


@Logges_cli.command(
    name="show",
    help="Show entered log file if exists.",
)
@click.option(
    "--file",
    "-f",
    required=True,
    help="Log file name. If you don't know please use " +
    click.style("show", fg="blue", underline=True, reverse=True) +
    " parameter.",
    callback=validate_file,
)
def show_log_file(file: Union[str, any]) -> None:
    """SHOW."""
    console_data(
        script_name=file,
        status_dict=Logges.LogStatus.get_blank_dict(),
        statuc_icon_dict=Logges.LogStatus.get_icon_dict(),
    )


@Logges_cli.command(name="search", help="Search and get file name which is contains given keyword(s)\
 or Sentence(s), Sentences splitted with ','.")
@click.option(
    "--max_date",
    required=False,
    help="Show logs of maximum date.",
    callback=validate_date,
)
@click.option(
    "--min_date",
    required=False,
    help="Show logs of minimum date.",
    callback=validate_date,
)
@click.option(
    "--sentences",
    "-s",
    required=True,
    help="Searching sentences, separated with ',' character.",
)
@click.option(
    "--export",
    "-e",
    default=True,
    required=False,
    help="Export your log file as exported_... .",
)
def search_in_log_files(max_date: str, min_date: str, sentences: str, export: bool) -> None:
    """Search keywords on log files."""
    log_file_list = []
    log_dir = os.path.split(__file__)[0]
    for each_file in os.listdir(log_dir):
        if ".log" in each_file:
            if (not isinstance(min_date, None)) and (not isinstance(
                    max_date, None)):
                if (each_file[:10] >= min_date) and (each_file[:10] <=
                                                     max_date):
                    log_file_list.append(each_file)
            elif not isinstance(min_date, None):
                if each_file[:10] >= min_date:
                    log_file_list.append(each_file)
            elif not isinstance(max_date, None):
                if each_file[:10] <= max_date:
                    log_file_list.append(each_file)
            else:
                log_file_list.append(each_file)

    sentence_list = sentences.split(',')
    for each_log in log_file_list:
        full_logfile_path = os.path.join(log_dir, each_log)
        file = open(full_logfile_path, "r")
        (
            _date_list,
            _status_list,
            _filename_list,
            _functname_list,
            _log_message_list,
        ) = extract_logs(logs=file)
        for each_log_msg in _log_message_list:
            for each_sentence in sentence_list:
                if each_sentence in each_log_msg:
                    pass

    pass


if __name__ == "__main__":
    Logges_cli()
