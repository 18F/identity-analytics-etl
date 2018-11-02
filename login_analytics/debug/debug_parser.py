# -*- coding: utf-8 -*-

import os
from src.event_parser import EventParser
from src.pageview_parser import PageViewParser
from src.device_parser import DeviceParser
from src.email_parser import EmailParser
from src.phone_parser import PhoneParser


def debug(test_log_file_path):
    """
    This function reproduce the parse behavior.

    Test if there is any:

    - events
    - events_devices
    - events_email
    - events_phone
    - pageviews
    """
    test_log_file_dirpath = os.path.dirname(test_log_file_path)
    with open(test_log_file_path, "rb") as f:
        source_file_n_rows = f.read().decode("utf-8").count("\n") + 1

    print("got {} rows to process ...".format(source_file_n_rows))
    parsers = (EventParser(), PageViewParser(), DeviceParser(), EmailParser(), PhoneParser())
    for parser in parsers:
        print("run {} ...".format(parser))
        (
            processed_rows,
            out,
            out_parquet
        ) = parser.stream_csv(open(test_log_file_path, "rb").read())
        print("  {} rows are parsed.")
        dst = os.path.join(
            test_log_file_dirpath,
            "{}_parse_result.csv".format(parser.table)
        )
        with open(dst, "w") as f:
            f.write(out.read())


if __name__ == "__main__":
    # specify your test log file
    test_log_file_path = ""
    debug(test_log_file_path)
