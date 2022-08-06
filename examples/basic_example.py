"""A simple example."""
from Logges import Logges
from other_module import other_method


if __name__ == '__main__':
    Logges.setup(__file__)
    Logges.log(log="A simple info method.", status=0, print_log=False)
    Logges.log(log="A simple warning method.", status=1, print_log=False)
    Logges.log(log="A simple error method.", status=2, print_log=False)
    other_method()
    Logges.to_markdown()
    Logges.to_pdf()
    Logges.console_data()
