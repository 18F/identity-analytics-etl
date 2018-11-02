.. contents::

.. _a-new-way-of-writing-docs:

A New Way of Writing Docs
==============================================================================


Disadvantage of Using WIKI
------------------------------------------------------------------------------

Github WIKI: https://github.com/18F/identity-analytics-etl/wiki

**Maintainability**:

- Hard to migrate / export / backup WIKI.
- Maintain same topic multiple place. Code is at one place, Doc at other place.
- Takes extra effort to maintain code / data related content (DRY, don't repeat yourself).

**Accessibility**:

- No full text search across entire project.
- Lack of cross page reference and link.


What is Doc Builder Tool
------------------------------------------------------------------------------

**What is Doc Builder**:

- Doc written in markdown or similar plain text markup language, **doc is part of the code repo**.
- Programmatically generate documentation in any format, html static website, pdf, latex and more.
- Deploy it anywhere. AWS S3, free third party doc site host, private server, or portable zip file.

**Famous project using doc builder**:

- AWS official doc: https://github.com/awsdocs/aws-lambda-developer-guide
- Mongodb official doc: https://github.com/mongodb/docs
- Python official doc: https://github.com/python/cpython

Using doc builder tools for IT project gradually becomes industry standard. `Sphinx Doc <http://www.sphinx-doc.org/en/master/>`_ is the most popular one.


Advantage of Using Doc Builder Tool
------------------------------------------------------------------------------

Solves all problems in Github WIKI, and provide additional productivity feature to ease maintenance and improve user experience.


**Maintainability**:

- Doc source as part of the code in Git repo. :strike:`Hard to migrate / export / backup WIKI`.
- Automatically extract comments, doc string from code. :strike:`Code is at one place, Doc at other place`.
- Programmatically generate document from data, for example, tabulate table. :strike:`Takes extra effort to maintain code / data related content (DRY, don't repeat yourself)`.


**Accessibility**:

- Built in full text search. For example, search: ``sql monthly signups``. :strike:`No full text search across entire project`.
- Powerful reference markup, reference or literal include anything. :strike:`Lack of cross page reference and link`.


**Additional Feature**:

- Deploy to S3, access control.
- Automatically Generate API document:
    - Code: https://github.com/MacHu-GWU/uszipcode-project/blob/master/uszipcode/search.py
    - Doc: https://uszipcode.readthedocs.io/py-modindex.html
- Adapt any HTML, CSS, Javascript feature. For example:
    - copy to clipboard
    - sortable table
    - css style control
    - embed anything: https://s3-us-west-2.amazonaws.com/login-gov-doc/login_analytics/03-Data-System-Maintainance/index.html
- Iterate Include:
    - markup: ``.. literalinclude:: /../../sql/analytics-query/time-series/monthly_signups.sql``
    - content: :ref:`aq_monthly_signups`
- Generate Docs from Data: `` .. tabulate-table:: data.json``


**Extra Effort**:

- Setup once, apply it everywhere.
- Non developer can write docs on Github or pull the source and working locally. As they usually do with Markdown.
- Code deployment is painless.
    - continually automatically build and deploy it for every commit / PR.
    - one command to deploy static site to AWS S3


Feature Example
------------------------------------------------------------------------------

Sortable Table:

.. list-table:: User Table
    :widths: 10 10
    :header-rows: 1
    :class: sortable

    * - id
      - name
    * - 1
      - Cathy
    * - 2
      - Alice
    * - 3
      - Bob

Copy to Snippet:

.. code-block:: SQL

    SELECT * FROM events LIMIT 10;

- this is :red:`red`
- this is :blue:`blue`
- this is :green:`green`


How to Maintain The Documentation
------------------------------------------------------------------------------
