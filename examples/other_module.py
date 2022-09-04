"""Outside module example."""
from Logges import Logges


def other_method():
    """Amazing eExample method."""
    Logges.log(msg="This log called from other module.", status=Logges.LogStatus.ERROR)
