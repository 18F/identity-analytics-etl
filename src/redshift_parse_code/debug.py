# -*- coding: utf-8 -*-

"""
This script help us to debug the parser.
"""

import os
from src.event_parser import EventParser
from src.pageview_parser import PageViewParser
from src.device_parser import DeviceParser
from src.email_parser import EmailParser
from src.phone_parser import PhoneParser


def debug():
    """
    Put your test log file at ./tmp.txt.
    """
    test_log_file_path = os.path.join(os.path.dirname(__file__), "tmp.txt")
    parsers = (EventParser(), PageViewParser(), DeviceParser(), EmailParser(), PhoneParser())
    for parser in parsers:
        parsed_rows, total_rows, out, out_parquet = parser.stream_csv(open(test_log_file_path, "rb").read())
        with open("{}.csv".format(parser.table), "w") as f:
            f.write(out.read())
        print(parser.table, parsed_rows)


if __name__ == "__main__":
    debug()
