.. _how-to-run-query-on-idp-db-in-ruby-console:

How To Run a Custom Query on IDP DB in Ruby Console
==============================================================================

.. contents::
    :local:


1. Get the Utility Shell Scripts from ``devops`` Repo
------------------------------------------------------------------------------

- Clone the repo: https://github.com/18F/identity-devops
- Setup your ruby following this guide: https://github.com/18F/identity-idp. Finally you should able to see your ruby version is 2.3.X by running ``ruby -v`` command.
- Setup your PIV card auth, follow this guide: https://github.com/18F/identity-private/wiki/Operations:-MacOSX-PIV-to-SSH-key-extraction. This should be already be done as part of your on-boarding process.


2. SSH to prod instance, log in to Ruby Console
------------------------------------------------------------------------------

1. Establish SSH to current IDP prod server (ec2 instance):

first:

.. code-block:: bash

    cd <path-to-identity-devops>

stay in root dir, and:

.. code-block:: bash

    ./bin/ssh-instance --newest asg-prod-idp

2. Once you have access to the IDP server, then get in ruby console:

first:

.. code-block:: bash

    cd /srv/idp/current

then:

.. code-block:: bash

    sudo -uwebsrv RAILS_ENV=production ALLOW_CONSOLE_DB_WRITE_ACCESS=true bundle exec rails c

or:

.. code-block:: bash

    sudo -uwebsrv RAILS_ENV=production bundle exec rails c

.. warning::

    By default, the ruby console uses a read-only account. However, if the goal is to execute write operations, you can set  ``ALLOW_CONSOLE_DB_WRITE_ACCESS=true`` to switch to write mode, assuming your account has the required privileges and role.

.. note::

    The read-only account doesn't have access to all of production tables, only access to tables that are mostly required for data analysis.


``id-rails-console`` is a short-cut command for ``sudo -uwebsrv RAILS_ENV=production bundle exec rails c``


3. Execute Query
------------------------------------------------------------------------------

Now you are in ruby console.

**Set Timeout Limit**:

By default ruby console use IDP app timeout setting, which is only 2 seconds. Set timeout to a higher value with this command:

.. code-block:: bash

    ActiveRecord::Base.connection.execute('SET statement_timeout = 120000')

**Run Query in SQL**:

.. code-block:: ruby

    tuples = ActiveRecord::Base.connection.execute('SELECT * FROM users LIMIT 3;')

**Run Query in ORM**:

.. code-block:: ruby

    tuples = User.limit(3)

**Export to csv to stdout**:

.. code-block:: ruby

    require 'csv'
    tuples.first.keys.to_csv
    tuples.each { |t| puts t.values.to_csv }
