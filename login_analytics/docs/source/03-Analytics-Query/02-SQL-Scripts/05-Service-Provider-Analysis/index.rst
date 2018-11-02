.. _sp-analysis:

Service Provider Analysis
==============================================================================

Because we charge service provider by successful login, number of signup / signin by SP is super important to login.gov. ``re-use rate`` (users with multiple SP) is another critical factor.


.. literalinclude:: ./no-sp-user-counts.sql
    :language: sql


.. literalinclude:: ./no-sp-user-list.sql
    :language: sql
