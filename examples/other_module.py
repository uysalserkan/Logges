"""Outside module example."""
from Logges import Logges


def other_method():
    """Amazing eExample method."""
    Logges.log(log="This log called from other module.", status=2, print_log=True)
