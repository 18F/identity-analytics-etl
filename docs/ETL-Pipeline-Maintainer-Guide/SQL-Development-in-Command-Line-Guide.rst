.. meta::
    :author: Sanhe Hu

.. _sql-development-in-command-line-guide:

SQL Development in Command Line Guide
==============================================================================

.. note::

    DON'T RUN EXPENSIVE QUERY ON PROD. Use:

    - limit returns: ``LIMIT 5``
    - use aggregate function: ``SELECT COUNT(*) FROM ... GROUP BY *``

Since we can't grant everyone sql client access, the sql developer has to SSH to secure server, then execute query via ``psql`` in command line interface.

Unlike using a sql client software, there is no **sql editor**, **tabulate data viewer**, **result export service** in psql shell.

Here's some tricks you can use to make your life easier.

.. contents::
    :local:


Edit Multi-Line Query
------------------------------------------------------------------------------

You should edit long query in any text editor, then copy and paste it in psql shell. Be careful about:

1. end query with ``;``
2. use 2/4/8 space instead of TAB for indent.

For example:

.. code-block:: SQL

    SELECT
        E.user_count as user_count,
        service_providers.friendly_name as sp_name,
        E.sp_uri as sp_uri,
    FROM
    (
        SELECT
            COUNT(identities.user_id) AS user_count,
            identities.service_provider AS sp_uri
        FROM identities
        GROUP BY identities.service_provider
    ) as E
    JOIN service_providers
    ON E.sp_uri = service_providers.issuer;


View Big Ascii Table
------------------------------------------------------------------------------

Psql returns the result in ascii table by default. But sometimes the width of the table is greater than the command line window. In this case you need to **toggle off line wrapping** in your terminal software.

For Mac, we have:

**Disable** line wrapping::

    tput rmam

**Enable** line wrapping::

    tput smam

Reference:

- https://stackoverflow.com/questions/28954083/how-to-turn-off-word-wrap-in-iterm2


Export Result to TSV File
------------------------------------------------------------------------------

``psql`` ASCII Table is very human-readable, but not friendly to machine. Writing the result to a csv file for further analysis is a better option. I recommend using TSV (Tab separate) over CSV in general. Because TSV is better for:

- ``,`` character escaping.
- Can be directly copy and paste to Excel / Google Sheet.

``psql`` has a built-in ``copy`` command https://www.postgresql.org/docs/current/sql-copy.html for this. This is an example of exporting data in TSV format::

    \copy (SELECT * FROM service_providers) to '/tmp/service_providers.csv' with (FORMAT CSV, HEADER, DELIMITER E'\t');

A problem is **\copy command DOES NOT support multi-line query**!

My solution is to **create a temp view** which can be declared over multiple lines, then select from it in the ``\copy`` command, which fits comfortably on one line.

Example (Replace the ``SELECT * FROM service_providers`` with custom query):

.. code-block:: sql

    CREATE TEMP VIEW v_temp AS (
        SELECT *
        FROM service_providers
    );
    \copy (SELECT * FROM v_temp) to '/tmp/service_providers.csv' with (FORMAT CSV, HEADER, DELIMITER E'\t');
    DROP VIEW v_temp;

Then you can find the result in TSV format at ``/tmp/service_providers.csv``.

Reference:

- https://stackoverflow.com/questions/42404579/use-psqls-copy-for-a-multi-line-query


Copy TSV Result to your Local Machine
------------------------------------------------------------------------------

By default, ipd server doesn't allows to transfer data out from it with the ``ssh`` command. But the ``identity-devops`` repo has a **command line tool** ``scp-instance`` can securely do that.

First, follow this :ref:`Guide <ssh-to-prod-server>`, **ssh to idp server**::

    ./bin/ssh-instance --newest asg-prod-idp

You should able to see the instance ID in the dialogue::

    I, [2018-12-10T14:06:02.132128 #55154]  INFO -- ssh-instance: SSH to "asg-prod-idp" (i-02d618ed7f9db11a2)

Then copy TSV file to your local machine::

    ./bin/scp-instance <instance-id>:<file-path-on-server> <destination-path>

In this example, it is::

    ./bin/scp-instance i-02d618ed7f9db11a2:/tmp/service_providers.csv ~/service_providers.csv
