# -*- coding: utf-8 -*-

from pathlib_mate import PathCls as Path


def generate_markup(root_dir):
    for file in Path(root_dir).select_by_ext(".sql"):
        pass
