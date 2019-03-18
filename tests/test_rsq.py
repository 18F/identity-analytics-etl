# -*- coding: utf-8 -*-

"""
create dummy credential file, create some test data.
"""

import os
import json

credential_file = os.path.join(os.path.expanduser("~"), ".db.json")

test_db_identifier = "18f-analytics-redshift"
test_db_credential = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "username": "postgres",
    "password": "password",
}


def save_credential_file(data):
    with open(credential_file, "wb") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True).encode("utf-8"))


def setup():
    if not os.path.exists(credential_file):
        data = {test_db_identifier: test_db_credential}
        save_credential_file(data)

    else:
        with open(credential_file, "rb") as f:
            data = json.loads(f.read().decode("utf-8"))
        if test_db_identifier not in data:
            data[test_db_identifier] = test_db_credential
            save_credential_file(data)


setup()


def create_test_data():
    import sqlalchemy as sa
    from sqlalchemy_mate import EngineCreator

    engine = EngineCreator.from_home_db_json(test_db_identifier) \
        .create_postgresql_psycopg2()
    metadata = sa.MetaData()
    t_users = sa.Table(
        "test_rsq_users", metadata,
        sa.Column("id", sa.Integer),
        sa.Column("name", sa.String),
    )
    metadata.create_all(engine)
    engine.execute(t_users.delete())

    t_users_data = [
        dict(id=1, name="Alice"),
        dict(id=2, name="Bob"),
        dict(id=3, name="Cathy"),
    ]
    engine.execute(t_users.insert(), t_users_data)


create_test_data()
