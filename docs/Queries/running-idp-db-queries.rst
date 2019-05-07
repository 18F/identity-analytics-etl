.. _running-idp-db-queries:

How To Run a Custom Query on IDP DB
==============================================================================

**IDB DB** is the production database serving login.gov website. It has less information than Redshift, but more accurate.

.. contents::
    :local:


1. Get the Utility Shell Scripts from ``devops`` Repo
------------------------------------------------------------------------------

- **Clone the devops repo**: https://github.com/18F/identity-devops
- **Setup your ruby** following this guide: https://github.com/18F/identity-idp. Finally you should able to see your ruby version is 2.3.X by running ``ruby -v`` command.
- **Setup your PIV card auth**, follow this guide: https://github.com/18F/identity-private/wiki/Operations:-MacOSX-PIV-to-SSH-key-extraction. This should be already be done as part of your on-boarding process.
- **Setup your AWS CLI**, follow this guide: https://aws.amazon.com/cli/. Configure your ``~/.aws/credentials`` and ``~/.aws/config``, put the ``identity-prod`` AWS Account API credential in it.


.. _ssh-to-prod-server:

2. SSH to prod server
------------------------------------------------------------------------------

Establish SSH to current IDP prod server (ec2 instance):

.. code-block:: bash

    cd <path-to-identity-devops> && export AWS_PROFILE=login.gov && ./bin/ssh-instance --newest asg-prod-idp


3.1 Access the ruby console
------------------------------------------------------------------------------

Once you have access to the IDP server, then get in ruby console:

first:

.. code-block:: bash

    cd /srv/idp/current && sudo -uwebsrv bundle exec rails c


``id-rails-console`` is a short-cut command for ``sudo -uwebsrv RAILS_ENV=production bundle exec rails c``


3.2 Access the db through psql shell
------------------------------------------------------------------------------
Psql app are not installed on idp server yet. You need to run this (With sudo) to install it:

.. code-block:: bash

    sudo apt-get install postgresql-client && cd /srv/idp/current && sudo -uwebsrv bundle exec rails dbconsole


There are only two db user accounts:

1. login.gov app
2. Read only account

Run this command (with ``identity-prod`` AWS Account IAM credential) on your local machine to get your db password:

.. code-block:: bash

    aws s3 cp ${APPLICATION_SECRET_URL} - | grep database_password

.. warning::

    Ensure you have permission to do this

Now you are in psql shell and ready for some SQL queries.


4. Execute Query in Ruby Console
------------------------------------------------------------------------------

Now you are in ruby console.

**Set Timeout Limit**:

By default ruby console use IDP app timeout setting, which is only 2 seconds. Set timeout to a higher value (in this example 120,000 millisecond) this command:

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