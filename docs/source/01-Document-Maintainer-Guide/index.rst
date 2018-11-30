Document Developer Guide
==============================================================================

.. contents::
    :depth: 1
    :local:

This articled is targeted for:

1. Non developer to help them understand how to contribute to docs and perform reviews for others.
2. Developers to understand how to maintain the doc generation system set up, build doc, host the doc.


If You Are Doc Writer
------------------------------------------------------------------------------

**Step by Step: Make changes to the Doc**:

**The Easy Way**:

1. Go to https://github.com/18F/identity-analytics-etl/tree/master/docs/source, or the anywhere you want to create the doc file.
2. Click button ``Create new file``.
3. Write content in ``<filename>.rst`` (`RST Syntax <https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst>`_, RECOMMENDED) or ``<filename>.md`` (Markdown Syntax)
4. Commit the change. Create a :red:`new branch` for this commit, naming convention is ``<your-name>/<purpose-of-this-branch>``.
5. Issue a `PR <https://github.com/18F/identity-analytics-etl/pulls>`_, ask other to do code review, deploy doc changes.

**The Preferred Way (if you need to continually update the docs)**:

1. Pull the latest code from `GitHub <https://github.com/18F/identity-analytics-etl>`_, create your own branch.
2. Writing the doc in ``.rst`` or ``.md``, put the file in ``./identity-analytics-etl/docs/source``, for example ``./identity-analytics-etl/docs/source/FY2019-business-analytics-metrics.rst`` (File Style) or ``./identity-analytics-etl/docs/source/FY2019-business-analytics-metrics/index.rst`` (Folder Style).
3. Issue a `PR <https://github.com/18F/identity-analytics-etl/pulls>`_, ask other to do code review, deploy doc changes.

If you are not familiar with Git / GitHub, read :ref:`use-github-client-to-update-docs`.

.. note::

    I highly recommend you write doc in RestructuredText instead of Markdown this is **WHY**: :ref:`md-vs-rst`.

    A short answer is:

    1. Markdown does not offer cross file link.
    2. 80% RST Syntax compatible with MD, the 20% includes **Header** and **Hyper Link**

    Header:

    .. code-block:: ReST

        Markdown:

        # Header1

        ## Header2

        ### Header3

        RST:

        Header1
        ==========

        Header2
        ----------

        Header3
        ~~~~~~~~~~

    Hyper Link::

        Markdown:

        [Google Homepage](www.google.com)

        RST:

        `Google Homepage <www.google.com>`_


If you Are Doc Maintainer
------------------------------------------------------------------------------

If you are familiar with `Sphinx Doc <https://www.sphinx-doc.org/>`_, skip this section. If you are NOT, read on.

    - :ref:`doc-maintenance-faq`
    - How to include a document to the place where it is needed?
    - How to build the doc site?
    - How to deploy the doc site?
    - :ref:`sphinx-doc-quick-explain`


If you Are Doing Doc Review
------------------------------------------------------------------------------

1. Go to the `Pull Request <https://github.com/18F/identity-analytics-etl/pull>`_, find the specific PR, for example, `This One <https://github.com/18F/identity-analytics-etl/pull/155>`_.
2. Click `Files Changed <https://github.com/18F/identity-analytics-etl/pull/155/files>`_, to see the file changes.
3. Click `View File <https://github.com/18F/identity-analytics-etl/blob/607c3c064413a7c1a23c52d071751326b2111ab5/docs/source/01-Document-Maintainer-Guide/index.rst>`_ on doc source file (usually ``.rst`` or ``.md``) to preview the doc.
4. Click on the line (the ``+`` icon), leave your comment and suggestion.
5. Finally, Click ``Review changes`` button to take an action in one of ``Comment``, ``Approve`` or ``Request changes``.

    .. image:: https://img.shields.io/badge/-Review_changes-brightgreen.svg



.. _why-sphinx-doc:

Why Sphinx Doc
------------------------------------------------------------------------------
We use `Sphinx Doc <https://www.sphinx-doc.org/>`_ builder tool to automatically generate our documentation site.

1. **Doc is part of the code, write once, deploy it to anywhere**. (The doc source file is sitting at ``identity-analytics-etl/docs/source/...``)
2. **Automatically extract comment and doc string from code, generate API document** (auto generated API docs is sitting at ``identity-analytics-etl/docs/source/login_analytics``).
3. No need to maintain same thing in TWO place.
4. Powerful feature set such as cross page reference, copy code to clipboard, auto table of content, literal including. Markdown and Github WIKI do not offer these.
