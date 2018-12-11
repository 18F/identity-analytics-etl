# -*- coding: utf-8 -*-

from .auto_sql_doc import AutoSqlDoc


def setup(app):
    app.add_directive("autosqldoc", AutoSqlDoc)
