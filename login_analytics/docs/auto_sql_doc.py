# -*- coding: utf-8 -*-

"""
This is an sphinx extension

This is how we organize sql file in file system::

    Analytics-Query
    |-- <Sql-Group-Name1>
        |-- <filename1>.sql
        |-- <filename2>.sql
        |-- ... (may have nested folder)

This extension will create a header for each sql group, and create a sub header
for each ``.sql`` file. Derives RST content like::

    SQL GROUP NAME 1
    ----------------

    table of content: ...

    filename1
    ~~~~~~~~~
    description ...

    .. code-block:: sql

        sql statement ...

    ...
"""

from __future__ import unicode_literals
import re
import sphinx.util
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
from pathlib_mate import PathCls as Path
from rstobj.markup import Header
from rstobj.directives import TableOfContent, CodeBlockSQL


COMMENT_PATTERN = re.compile("/\*[\s\S]*\*/")
root = Path("/Users/sanhehu/Documents/GitHub/identity-analytics-etl/docs/source/02-Analytics-Query")


def extract_comment_and_sql(content):
    """
    Separate comment and SQL statement from a sql file.
    Comment block is the text in ``/* <comment-block> */``

    :param content: str
    :return: comment, str; sql_state, str;
    """
    comment_blocks = re.findall(COMMENT_PATTERN, content)
    comment = "\n\n".join([
        block[2:-2].strip() for block in comment_blocks
    ]).strip()
    for cmt in comment_blocks:
        content = content.replace(cmt, "\n\n")
    sql_stat = content.strip()
    return comment, sql_stat


def generate_rst(root_dir):
    """
    Generate RST content, including all ``.sql`` content, and organize them
    in a proper way.

    :param root_dir: ``pathlib.Path``, The root directory.
        usually it is the ``Analytics-Query`` folder.
    :return: rst text.
    """

    def filters(p):
        if (p.ext == ".sql") and (p.parent.basename != "draft"):
            return True
        else:
            return False

    group_set = set()  # sql group duplicate filter
    rst_lines = list()
    for p in Path.sort_by_abspath(root_dir.select_file(filters)):
        rel_path = p.relative_to(root)
        relative_parts = rel_path.parts

        # create a header2 for sql group, and auto index items
        group_title = relative_parts[0]
        if group_title not in group_set:
            header = Header(title=group_title, header_level=2, auto_label=True)
            rst_lines.append(header.render())
            toc = TableOfContent(local=True)
            rst_lines.append(toc.render())
            group_set.add(group_title)

        # file name to be the title
        header_title = p.fname
        header = Header(title=header_title, header_level=3, auto_label=True)
        rst_lines.append(header.render())
        comment, sql_stat = extract_comment_and_sql(content=p.read_text("utf-8"))
        # comment to be the body text
        rst_lines.append(comment)

        # sql_stat to be the code snippet
        code_block = CodeBlockSQL.from_string(sql_stat)
        rst_lines.append(code_block.render())

    rst = "\n\n".join(rst_lines)
    return rst


class AutoSqlDoc(Directive):
    """
    Implement ``autosqldoc`` directive::

        .. autosqldoc::
    """
    has_content = False

    def run(self):
        node = nodes.Element()
        node.document = self.state.document
        current_file = self.state.document.current_source
        output_rst = generate_rst(Path(current_file).parent)
        view_list = StringList(output_rst.splitlines(), source='')
        sphinx.util.nested_parse_with_titles(self.state, view_list, node)
        return node.children
