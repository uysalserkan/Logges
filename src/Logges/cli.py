"""CLI app."""
import os
import click

from datetime import datetime
from typing import Union
from Logges import Logges

from .utils import extract_logs
from .utils import console_data
from .utils import to_pdf


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
)
@click.option(
    "--local_file",
    default=False,
)
def show_log_file(file: Union[str, any], local_file: bool) -> None:
    """SHOW."""
    if not local_file:
        validate_file(None, None, value=file)
    else:
        file = os.path.abspath(file)
    console_data(
        script_name=file,
        status_dict=Logges.LogStatus.get_blank_dict(),
        statuc_icon_dict=Logges.LogStatus.get_icon_dict(),
        local_file=local_file,
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
    "-sen",
    required=True,
    help="Searching sentences, separated with ',' character.",
)
@click.option(
    "--functions",
    "-fu",
    required=False,
    default=None,
    help="Searching functions, separated with ',' character.",
)
@click.option(
    "--status",
    "-sta",
    required=False,
    default=None,
    help="Searching status, separated with ',' character.",
)
@click.option(
    "--files",
    "-fi",
    required=False,
    default=None,
    help="Searching status, separated with ',' character.",
)
@click.option(
    "--export_name",
    required=False,
    help="Set your export log file.",
)
@click.option(
    "--export",
    "-e",
    default=None,
    required=False,
    help="You can export your search result as log, md and pdf (only one type).",
)
def search_in_log_files(
    max_date: str,
    min_date: str,
    sentences: str,
    functions: str,
    status: str,
    files: str,
    export_name: str,
    export: str,
) -> None:
    """Search keywords on log files."""
    # Writting in file
    if export:
        if export.lower() not in ["log", "pdf", "md"]:
            raise click.BadOptionUsage(
                option_name="export",
                message="Please enter a " + click.style(text="valid ", fg="red", blink=True)
                + " export type like: " + click.style(text="log, md, pdf", underline=True)
            )

    if export_name:
        tmp_filename = f"{export_name}.log"
    else:
        tmp_filename = datetime.now().strftime("Export %Y-%m-%d %H%M%S.log")
    tmp_file = open(tmp_filename, "w")

    # Log files
    log_file_list = []
    log_dir = os.path.split(__file__)[0]
    for each_file in os.listdir(log_dir):
        if ".log" in each_file:
            if (not isinstance(min_date, type(None))) and (not isinstance(
                    max_date, type(None))):
                if (each_file[:10] >= min_date) and (each_file[:10] <=
                                                     max_date):
                    log_file_list.append(each_file)
            elif not isinstance(min_date, type(None)):
                if each_file[:10] >= min_date:
                    log_file_list.append(each_file)
            elif not isinstance(max_date, type(None)):
                if each_file[:10] <= max_date:
                    log_file_list.append(each_file)
            else:
                log_file_list.append(each_file)

    # Create list of params, separated with ','
    if sentences:
        sentence_list = sentences.split(',')

    if status:
        status_list = status.split(',')

    if functions:
        functions_list = functions.split(',')

    if files:
        files_list = files.split(',')

    # Extract and filter logs.
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

        each_tmp_log_file = open(each_log, 'w')
        counter = 0

        for index, each_log_msg in enumerate(_log_message_list):
            if sentence_list:
                for each_sentence in sentence_list:
                    if each_sentence in each_log_msg:
                        if status:
                            if _status_list[index].replace('[', '').replace(']', '') not in status_list:
                                continue

                        if functions:
                            clear_funct_name = _functname_list[index].replace('[', '')\
                                                                     .replace(']', '')\
                                                                     .replace('<', '')\
                                                                     .replace('>', '').split(':')[0]
                            if clear_funct_name not in functions_list:
                                continue

                        if files:
                            if _filename_list[index].replace('[', '').replace(']', '') not in files_list:
                                continue
                        tmp_file.write(
                            f"{_date_list[index]} [{_status_list[index].replace('[', '').replace(']', '') :8s}] " +
                            f"{_filename_list[index]} {_functname_list[index]}:({each_log}) {_log_message_list[index]}"
                        )
                        each_tmp_log_file.write(
                            f"{_date_list[index]} [{_status_list[index].replace('[', '').replace(']', '') :8s}] " +
                            f"{_filename_list[index]} {_functname_list[index]}: {_log_message_list[index]}"
                        )
                        counter += 1
        if counter > 0:
            # Close temp file for writting on console log.
            each_tmp_log_file.close()

            console_data(
                script_name=each_log,
                status_dict=Logges.LogStatus.get_blank_dict(),
                statuc_icon_dict=Logges.LogStatus.get_icon_dict(),
                local_file=True,
            )

        # Remove temp log file.
        os.remove(each_log)

    tmp_file.close()

    if not export:
        os.remove(tmp_filename)
    else:
        if export.lower() == 'md':
            pass
        elif export.lower() == 'pdf':
            to_pdf(
                script_name=tmp_filename,
                saving_path='.',
                status_dict=Logges.LogStatus.get_blank_dict(),
                local_file=True
            )
            os.remove(tmp_filename)
            os.remove("pie_chart.png")


if __name__ == "__main__":
    Logges_cli()
