#!/bin/bash
#
# ERAlchemy command for generating ERD: https://pypi.org/project/ERAlchemy/
# Postgresql connection string format: https://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2
#
# NOTE:
#
# IDP DB doesn't use foreign key constrain explicitly, the relationship
# are managed by Ruby app. That's why the output only has schema but not relationship.

PACKAGE_NAME="login_analytics"
ROOT_DIR=$(git rev-parse --show-toplevel)
BIN_ERAlchemy=${ROOT_DIR}/${PACKAGE_NAME}_venv/bin/eralchemy
${BIN_ERAlchemy} -i postgresql+psycopg2://${USER}:@localhost:5432/upaya_development -o erd-from-idp-db.pdf