.. _sphinx-doc-quick-explain:

Sphinx Doc Quick Explain
==============================================================================

**This documentation is for developer that does know much about** `sphinx doc <http://www.sphinx-doc.org/en/master/>`_, **but want know how to use it correctly to generate beautiful, self managed doc site**.

**Important directory and file**:

- repo root dir (alias ``repo-root``): ``identity-analytics-etl/``
- doc source dir (alias ``doc-root``): ``identity-analytics-etl/docs/source/``.
- image, icon, css, javascripts, and all static files: ``<doc-root>/_static``, this path should NOT be modified.
- sphinx doc generator settings file: ``<doc-root>/conf.py``
- the generator scripts: ``<repo-root>/docs/Makefile`` for MacOS and Linux, ``<repo-root>/docs/make.bat`` for Windows.


Generate Documentation Static Site (Build Doc)
------------------------------------------------------------------------------

This command will generate the doc site in ``<repo-root>/docs/build/html/index.html``::

    $ cd <repo-root>/docs
    $ make html

You should see something like::

    Running Sphinx v1.8.1
    updating environment:
    reading sources...
    preparing documents...
    writing output...
    generating indices...
    build succeeded, xxx warnings.

- **Success**: if you see the ``build succeeded``, you can ignore most of warnings. Usually, it means you defined a link label, but never used, which is totally fine. **Occasional typo or RST/MD syntax error will NOT STOP the build**.
- **Failed**: if you didn't see the ``build succeeded``. Usually, it means your config file ``conf.py`` is not correctly setup, could be Python syntax error, could be variable definition error, import error.


The ``conf.py`` file
------------------------------------------------------------------------------

It is the configuration file, and it is actually a Python scripts. You can define:

1. Theme to use.
2. Extension to use.
3. Programmatically generate doc parts and do any black magic you want.
