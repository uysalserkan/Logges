"""A simple test file."""
from ..src.Logges.logges import Logges

if __name__ == '__main__':
    Logges.log(log='This is a test file', status=0, print_log=True)
    Logges.to_markdown()
