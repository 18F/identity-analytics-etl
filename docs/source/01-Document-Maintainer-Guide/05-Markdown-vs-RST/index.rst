.. _md-vs-rst:

Markdown vs RST
==============================================================================
**Markdown and reStructuredText (RST)** are two lightweight markup languages with plain text formatting syntax designed for easy input with any text editor, typically used for technical documentation as they emphasize plain-text readability. Both are widely used for API documentation, RST in Sphinx, the standard Python documentation system, and Markdown in Doxygen (optionally), MkDocs, the Rust Standard Library documentation, and other. Most developers are familiar with Markdown, however.

reStructuredText is a file format for textual data used primarily in the Python programming language community for technical documentation. Both Markdown and RST are lightweight markup language. **The RST syntax is very similar to Markdown**, You can think of RST as a super set of Markdown, RST offers everything Markdown does, but not vice versa.

.. list-table:: **Why use RST instead of Markdown**
    :widths: 10 10
    :header-rows: 1

    * - Features that RST has but Markdown does NOT
      - Why this feature is useful
    * - Include other doc content
      - Help us break large doc into smaller piece, better maintainability.
    * - Cross reference anywhere in the entire project.
      - url link may change. Use a unique identifier label to link is more stable.
    * - Programmatically generate doc content from data.
      - Maintaining the data at two place in the code and in the doc is not good.

**Even though it is recommended to use RST for consistency and the feature benefits, but it is OK to use Markdown as well if that's what you prefer**

For more information about writing docs in RST, check out:

- RST Cheatsheet: https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst
- RST Quick Ref: http://docutils.sourceforge.net/docs/user/rst/quickref.html
