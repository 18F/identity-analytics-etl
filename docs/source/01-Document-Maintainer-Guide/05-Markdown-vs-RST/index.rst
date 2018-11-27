.. _md-vs-rst:

Markdown vs RST
==============================================================================
In this project, doc writer can write docs in **either Markdown or RestructuredText** (RST).

I believe most of people are familiar with Markdown, maybe not for RST.

reStructuredText is a file format for textual data used primarily in the Python programming language community for technical documentation. Both Markdown and RST are lightweight markup language. **The RST syntax is very similar to Markdown**, You can think RST as a super set of Markdown, RST has everything in Markdown, but Markdown doesn't.

.. list-table:: **Why RST**
    :widths: 10 10
    :header-rows: 1

    * - Feature that RST has but Markdown NOT
      - Why this feature useful
    * - Include other doc content
      - Help us break large doc into smaller piece, better maintainability.
    * - Cross reference anywhere in the entire project.
      - url link may change. Use a unique identifier label to link is more stable.
    * - Programmatically generate doc content from data.
      - Maintaining the data at two place in the code and in the doc is not good.

**It is OK to write your doc in Markdown, but some design pattern will not be available**

For more information about writing docs in RST:

- RST Cheatsheet: https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst
- RST Quick Ref: http://docutils.sourceforge.net/docs/user/rst/quickref.html
