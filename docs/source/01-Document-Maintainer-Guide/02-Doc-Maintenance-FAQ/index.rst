.. _doc-maintenance-faq:

Doc Maintenance FAQ
==============================================================================

.. contents::
    :local:


Where is the link for the doc site?
------------------------------------------------------------------------------

The docs are deployed to https://s3-us-west-2.amazonaws.com/login-gov-doc/login_analytics/index.html. This website can be only accessed from GSA network. You need to connect to GSA VPN to visit the docs.


Where is the source file for the doc?
------------------------------------------------------------------------------

- https://github.com/18F/identity-analytics-etl/tree/master/docs/source


How can I view the changes after I updated the doc source?
------------------------------------------------------------------------------

.. code-block:: bash

    # this will rebuild the doc site locally
    $ make build_doc

    # view changes
    $ make view_doc


How can I deploy the latest docs?
------------------------------------------------------------------------------

.. code-block:: bash

    $ make deploy_doc
