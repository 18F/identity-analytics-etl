# -*- coding: utf-8 -*-

"""
This script transform `PostgreSQL ASCII table <https://www.postgresql.org/docs/current/static/tutorial-select.html>`_ into TSV (Tab Separate) format. You can directly copy TSV content to Excel or GoogleSheet.

From::

     user_id |  name
    ---------+--------
        1    |  Alice
        2    |   Bob

To::

    user_id name
    1   Alice
    2   Bob

And::

    user_id,name
    1,Alice
    2,Bob
"""

from __future__ import print_function
from io import StringIO

import pandas as pd


def strip_string(s):
    try:
        return s.strip()
    except:
        return s


def transform_to_csv(src):
    with open(src, "rb") as f:
        print("read data from '%s' ..." % src)
        content = f.read().decode("utf-8")
        lines = content.split("\n")
        del lines[1]  # remove second line
        content = "\n".join(lines)

        print("got %s rows, convert to data frame ..." % (len(lines) - 1,))
        buffer = StringIO()
        buffer.write(content)
        buffer.seek(0)
        df = pd.read_csv(buffer, sep="|")

        # strip white space
        df.columns = [c.strip() for c in df.columns]
        for c, t in df.dtypes.items():
            if str(t) == "object":
                df[c] = df[c].map(strip_string)

        dst = os.path.splitext(src)[0] + ".tsv"
        df.to_csv(dst, index=False, sep="\t")

        dst = os.path.splitext(src)[0] + ".csv"
        print("dump csv to '%s' ..." % dst)
        df.to_csv(dst, index=False, sep=",")

        print("complete!")


if __name__ == "__main__":
    import os

    HOME = os.path.expanduser("~")
    src = "tmp/tmp.txt"
    transform_to_csv(src)
