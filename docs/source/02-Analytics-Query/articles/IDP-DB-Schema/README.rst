Generate IDP DB Schema / ERD
==============================================================================

An user friendly IDP DB Schema manual is a must have document for developer.

To create the manual:

1. Setup the dev/test idp db locally.
2. Programmatically generate the Schema manual and `ER Diagram <https://www.visual-paradigm.com/guide/data-modeling/what-is-entity-relationship-diagram/>`_.


Setup dev/test idp db locally
------------------------------------------------------------------------------

1. Clone the repo: https://github.com/18F/identity-idp
2. Follow the instruction on https://github.com/18F/identity-idp, install ``ruby``, ``node``, ``redis``, ``postgres``.
3. run ``make setup``, now a dev/test db is available to connect.


Programmatically generate the Schema manual
------------------------------------------------------------------------------

- ``create_rst.py``: generate the table, column definition.
- ``create-erd.sh``: generate the ERD pdf. (Not available right now)

If there's any schema change, just run these two scripts again before you build the doc.
