"""A simple example."""
from Logges import Logges
from other_module import other_method


if __name__ == '__main__':
    Logges.setup()
    Logges.log(log="A simple DEBUG method.", status=Logges.LogStatus.DEBUG)
    Logges.log(log="A simple INFO method.", status=Logges.LogStatus.INFO)
    Logges.log(log="A simple WARNING method.", status=Logges.LogStatus.WARNING)
    Logges.log(log="A simple ERROR method.", status=Logges.LogStatus.ERROR)
    Logges.log(log="A simple CRITICAL method.", status=Logges.LogStatus.CRITICAL)
    other_method()
    Logges.export(markdown=True, pdf=True, log=True, zip=True)
