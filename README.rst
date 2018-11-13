.. image:: https://img.shields.io/badge/Link-Document-blue.svg
      :target: https://s3-us-west-2.amazonaws.com/login-gov-doc/login_analytics/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
      :target: https://s3-us-west-2.amazonaws.com/login-gov-doc/login_analytics/py-modindex.html

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/18f/identity-analytics-etl

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
      :target: https://github.com/18f/identity-analytics-etl/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
      :target: https://github.com/18f/identity-analytics-etl/issues


Welcome to ``login_analytics`` Documentation
==============================================================================

https://login.gov analytics code repo. Source code for:

- Data ETL Pipeline
- Analytics Query
- Machine Learning Model

Notes on 2018-11-07:

    This project used to be the source code for `Redshift ETL pipeline <https://github.com/18F/identity-analytics-etl/tree/master/legacy_code>`_. We need a redesign to have a all-in-one solution for managing all kinds of analytics related work. The ETL pipeline will be an sub module of this project.


Local development
------------------------------------------------------------------------------
Since AWS lambda only supports Python3.6 and Python2.7, so we use Python3.6 for development.

If it is your new Mac laptop, run this to set up your development environment::

    $ bash ./bin/setup-mac.sh

- ROOT/.python-version: This file is used by pyenv to specify global version of Python to be used in all shells. Reference: https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-global .
