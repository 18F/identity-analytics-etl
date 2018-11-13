# -*- coding: utf-8 -*-

"""
This scripts fix code style into pep8 style, https://www.python.org/dev/peps/pep-0008/
"""

from __future__ import print_function
from pathlib_mate import Path
from setup import package


def fixcode(**kwargs):
    """
    auto pep8 format all python file in ``source code`` and ``tests`` dir.
    """
    # repository direcotry
    repo_dir = Path(__file__).parent.absolute()

    # source code directory
    source_dir = Path(repo_dir, package.__name__)

    if source_dir.exists():
        print("Source code locate at: '%s'." % source_dir)
        print("Auto pep8 all python file ...")
        source_dir.autopep8(**kwargs)
    else:
        print("Source code directory not found!")

    # unittest code directory
    unittest_dir = Path(repo_dir, "tests")
    if unittest_dir.exists():
        print("Unittest code locate at: '%s'." % unittest_dir)
        print("Auto pep8 all python file ...")
        unittest_dir.autopep8(**kwargs)
    else:
        print("Unittest code directory not found!")

    print("Complete!")


if __name__ == "__main__":
    fixcode()