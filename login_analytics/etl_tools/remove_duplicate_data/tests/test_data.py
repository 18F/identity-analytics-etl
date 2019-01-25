# -*- coding: utf-8 -*-

"""
Generate random test data.
"""

import numpy as np
import random
import rolex


def random_datetime_array(n, start, end):
    """
    Generate n random datetime between (`start`, `end`)

    **High Performance**

    :param n: number of item
    :param start: str / datetime / timestamps, lower bound
    :param end: str / datetime / timestamps, upper bound
    :return: a generator
    """
    start_ts = rolex.to_utctimestamp(rolex.parse_datetime(start))
    end_ts = rolex.to_utctimestamp(rolex.parse_datetime(end))
    array = np.random.rand(n) * (end_ts - start_ts) + start_ts
    return (rolex.from_utctimestamp(ts) for ts in array)


def create_test_data(n_event, duplicate_perc, start, end):
    """
    Create benchmark test data

    :param n_event: number of rows in event table
    :param duplicate_perc: duplicates percentage
    :param start: start time
    :param end: end time
    :return: list of dict
    """
    t_event_data = [
        {"id": "id%s" % i, "time": dt}
        for i, dt in enumerate(random_datetime_array(n_event, start, end))
    ]
    dupe_data = random.sample(t_event_data, int(n_event * duplicate_perc))
    t_event_data.extend(dupe_data)
    random.shuffle(t_event_data)
    return t_event_data



if __name__ == "__main__":
    from sfm.timer import Timer
    n_event = 1000000
    duplicate_perc = 0.1
    start = "2018-01-01"
    end = "2018-12-31 23:59:59"

    with Timer():
        create_test_data(n_event, duplicate_perc, start, end)