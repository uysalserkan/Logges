"""There are some functions used in logges."""

import os
import matplotlib.pyplot as plt


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
