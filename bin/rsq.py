# -*- coding: utf-8 -*-

"""
This script:

1. read connection info from ~/.db.json file
2. find sql file path by query name

Set up:

first, create a ``~/.db.json`` file, put the following content::

    {
        "18f-analytics-redshift": {
            "host": "www.xxx.com",
            "port": 5432,
            "database": "...",
            "username": "...",
        }
    }
"""

__doc__ = """
Usage:

1. get db credential from ~/.db.json file: ``python rsq.py read_credential host|port|database|username``
2. get sql file path by name: python rsq.py get_sql auth_funnel
3. get all available query name: python rsq.py get_sql -l
"""

import os
import json

#--- command: read_credential
credential_file = os.path.join(os.path.expanduser("~"), ".db.json")
db_identity = "18f-analytics-redshift"
with open(credential_file, "rb") as f:
    credential_data = json.loads(f.read().decode("utf-8"))

#--- command: get_sql
if os.getcwd() in __file__:
    path_this = __file__
else:
    path_this = os.path.join(os.getcwd(), __file__)
dir_bin = os.path.dirname(path_this)
dir_project_root = os.path.dirname(dir_bin)
dir_doc_source = os.path.join(dir_project_root, "docs", "source")


def find_sql_by_filename(filename):
    """
    Find specific sql file path by its filename

    :param filename: str, xxx.sql
    :return: absolute path of a sql file
    """
    if not filename.lower().endswith(".sql"):
        raise ValueError("filename has to endswith .sql")
    for current_dir, _, file_list in os.walk(dir_doc_source):
        for fname in file_list:
            if fname == filename:
                return os.path.join(current_dir, filename)
    raise ValueError("{} NOT FOUND!".format(filename))


class SqlFileCollection(object):
    """
    Define query name and its sql file name
    """
    test_rsq = find_sql_by_filename("test_rsq.sql")
    auth_funnel = find_sql_by_filename("Authentication-Funnel.sql")

    @classmethod
    def _display_all_query(cls):
        for attr, value in cls.__dict__.items():
            if not attr.startswith("_"):
                print("{}: {}".format(attr, value))

    @classmethod
    def _get_sql_path_by_name(cls, name):
        return getattr(cls, name)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3:
        command = sys.argv[1]
        arg = sys.argv[2]

        if command == "read_credential":
            field = arg
            if field not in ["host", "port", "database", "username"]:
                raise ValueError("please specify one of 'host' | 'port' | 'database' | 'username'")
            else:
                print(credential_data[db_identity][field])

        elif command == "get_sql":
            query_name = arg
            if query_name == "-l":
                SqlFileCollection._display_all_query()
            else:
                print(SqlFileCollection._get_sql_path_by_name(query_name))

        else:
            raise ValueError("{} is not a valid command".format(command))
    else:
        print(__doc__)
