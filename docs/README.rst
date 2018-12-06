``<project-root>/docs`` Directory Explains
==============================================================================

- ``source``: doc source files.
- ``draft``: new docs, but haven't integrated into doc site yet.
- ``build``: a temp folder, never checked in to Git. doc site will be generated here locally to preview.
- ``Makefile`` and ``make.bat``: doc site generator scripts. Automatically been created from ``sphinx-quickstart`` command.


New Doc Writing Workflow
------------------------------------------------------------------------------

1. Put new docs in ``<project-root>/docs/draft``, then issue a Pull Request.
2. Decide where this doc should go to, figure out the endpoint of the page.
3. Put it under corresponding directory and properly reference it.
4. Generate the doc site, preview it.
5. If looks good, issue a Pull Request.

You can only issue ONE PR if the writer knows how to integrate it.