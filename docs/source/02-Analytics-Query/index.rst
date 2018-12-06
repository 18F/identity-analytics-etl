.. _analytics-query:

Analytics Query
==============================================================================

We use sphinx-doc automatically generating analytics queries. The doc builder will automatically scan ``.sql`` file in ``Analytics-Query`` directory, extract doc and sql statement, then organize them in a human readable and searchable way.

Please make sure there is only one sql for each file. And put all corresponding document in :ref:`RST syntax <md-vs-rst>` between ``/* document ... */``. And you can also put the description for entire user group in the ``README.rst`` file.

.. code-block:: bash

    02-Analytics-Query/
    |--- <query-group>/
         |--- <query-file>.sql
         |--- ... a lot .sql
         |--- README.rst or .md #
    ... a lot more query groups

.. code-block:: SQL

    /*
    Put the doc here.
    */

    SELECT COUNT(*) FROM users;


For Admin Console (Blazer App) User
------------------------------------------------------------------------------

You can find queries :ref:`query-lookup` for most of business metrics.

If you CAN NOT find the query you need, here's the way to request:

1. Go to https://github.com/18F/identity-analytics-etl/new/master/docs/source/02-Analytics-Query/draft, click  ``Create new file``, and create a ``human-readable-title.sql`` file.
2. Copy and paste the content from https://github.com/18F/identity-analytics-etl/blob/master/docs/source/02-Analytics-Query/draft/template.sql, fill in your description.
3. Create a new ``Pull Request``, and fill the code commit message.
4. Then the developer will get notified.

