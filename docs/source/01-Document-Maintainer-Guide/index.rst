Document Developer Guide
==============================================================================

.. contents::
    :depth: 1
    :local:


If You Are Doc Writer
------------------------------------------------------------------------------

**Step by Step: Make changes to the Doc**:

1. Pull the latest code from `GitHub <https://github.com/18F/identity-analytics-etl>`_, create your own branch.
2. Writing the doc in ``.rst`` or ``.md``, put the file in ``./identity-analytics-etl/docs/source``, for example ``./identity-analytics-etl/docs/source/FY2019-business-analytics-metrics.rst`` (File Style) or ``./identity-analytics-etl/docs/source/FY2019-business-analytics-metrics/index.rst`` (Folder Style).
3. Issue a `PR <https://github.com/18F/identity-analytics-etl/pulls>`_, code review, deploy doc changes.

If you are not familiar with Git / GitHub, read :ref:`use-github-client-to-update-docs`.

.. note::

    I highly recommend you write doc in RestructuredText instead of Markdown this is **WHY**: :ref:`md-vs-rst`.

    A short answer is:

    1. Markdown DOESN't HAVE CROSS FILE LINK.
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

1. If you are familiar with `Sphinx Doc <https://www.sphinx-doc.org/>`_, skip this section.
2. If you are NOT, and want to know:
    - :ref:`doc-maintenance-faq`
    - How to include a document to the place where it is needed?
    - How to build the doc site?
    - How to deploy the doc site?
    - :ref:`sphinx-doc-quick-explain`


.. _why-sphinx-doc:

Why Sphinx Doc
------------------------------------------------------------------------------
We use `Sphinx Doc <https://www.sphinx-doc.org/>`_ builder tool to automatically generate our documentation site.

1. **Doc is part of the code, write once, deploy it to anywhere**. (The doc source file is sitting at ``identity-analytics-etl/docs/source/...``)
2. **Automatically extract comment and doc string from code, generate API document** (auto generated API docs is sitting at ``identity-analytics-etl/docs/source/login_analytics``).
3. No need to maintain same thing in TWO place.
4. More powerful feature we really need such as, cross page reference, copy code to clipboard, auto table of content, literal including. Markdown and Github WIKI doesn't have it.
