from collections import namedtuple
from sqlalchemy.ext import compiler
from sqlalchemy.dialects.postgresql.base import PGIdentifierPreparer as pg

import sqlalchemy as sql


class Queries:

    def __init__(self):
        self.create_events = """CREATE TABLE events (
                                  id VARCHAR(40) NOT NULL,
                                  name VARCHAR(255) NOT NULL,
                                  user_agent VARCHAR(255),
                                  user_id VARCHAR(40),
                                  user_ip VARCHAR(50),
                                  host VARCHAR(255),
                                  visit_id VARCHAR(40),
                                  visitor_id VARCHAR(40),
                                  time TIMESTAMP,
                                  event_properties VARCHAR(4096),

                                  success BOOLEAN,
                                  existing_user BOOLEAN,
                                  otp_method VARCHAR(20),
                                  context VARCHAR(20),
                                  method VARCHAR(20),
                                  authn_context VARCHAR(50),
                                  service_provider VARCHAR(255),
                                  loa3 BOOLEAN,
                                  active_profile BOOLEAN,
                                  errors VARCHAR(4096));"""

        self.drop_events = """DROP TABLE IF EXISTS events;"""

        self.create_uploaded_files = """CREATE TABLE uploaded_files (
                                        s3filename VARCHAR(100) NOT NULL,
                                        destination VARCHAR(100) NOT NULL,
                                        uploaded_at TIMESTAMP,

                                        PRIMARY KEY(s3filename, destination));"""

        self.drop_uploaded_files = """DROP TABLE IF EXISTS uploaded_files;"""

        self.create_pageviews = """CREATE TABLE pageviews (
                                    method VARCHAR(10) NOT NULL,
                                    path TEXT,
                                    format VARCHAR(15),
                                    controller VARCHAR(100),
                                    action VARCHAR(15),
                                    status SMALLINT,
                                    duration FLOAT,
                                    user_id VARCHAR(40),
                                    user_agent VARCHAR(255),
                                    ip VARCHAR(50),
                                    host VARCHAR(255),
                                    timestamp TIMESTAMP,
                                    uuid VARCHAR(64) NOT NULL
                                    );"""

        self.drop_pageviews = """DROP TABLE IF EXISTS pageviews;"""

        self.create_user_agents = """CREATE TABLE user_agents (
                                        user_agent VARCHAR(255) NOT NULL,
                                        browser VARCHAR(100),
                                        platform VARCHAR(100),
                                        version VARCHAR(100),

                                        PRIMARY KEY(user_agent)
                                      );"""

        self.drop_user_agents = """DROP TABLE IF EXISTS user_agents;"""

        self.get_uploaded_files = """SELECT s3filename
                                     FROM uploaded_files;"""

        self.mark_uploaded = """INSERT INTO uploaded_files (s3filename, destination, uploaded_at)
                                VALUES ('{}', '{}', '{}');"""

        # TODO: Switch to SQLAlchemy ORM in #3

        self.load_csv_redshift = """COPY {table_name} ({columns})
                            FROM :filepath
                            IAM_ROLE :iam_role
                            REGION :region
                            FORMAT AS CSV IGNOREHEADER 1;"""

        self.load_csv = """COPY {table_name} ({columns})
                            FROM :filepath
                            CSV HEADER;"""

    def get_load_csv(self, table, columns, filepath):
        columns =  ', '.join(
            '"{}"'.format(column) for column in columns
        )
        table_name = '"{}"'.format(table)

        q = self.load_csv.format(table_name=table_name, columns=columns)
        query = sql.text(q)
        query = query.bindparams(
            sql.bindparam(
                'filepath',
                value=filepath,
                type_=sql.String,
        ))

        return query

    def get_load_csv_redshift(self, table, columns, filepath, iam_role, region):
        columns =  ', '.join(
            '"{}"'.format(column) for column in columns
        )
        table_name = '"{}"'.format(table)

        bindparams = [
                sql.bindparam(
                    'filepath',
                    value=filepath,
                    type_=sql.String,
                ),
                sql.bindparam(
                    'iam_role',
                    value=iam_role,
                    type_=sql.String,
                ),
                sql.bindparam(
                    'region',
                    value=region,
                    type_=sql.String,
                )
        ]

        q = self.load_csv_redshift.format(
                table_name=table,
                columns=columns
            )

        query = sql.text(q).bindparams(*bindparams)
        return query

    def get_build_queries(self):
        BuildQueries = namedtuple('BuildQueries', [
            'create_events',
            'create_uploaded_files',
            'create_pageviews',
            'create_user_agents'
        ])

        return BuildQueries._make([
            self.create_events,
            self.create_uploaded_files,
            self.create_pageviews,
            self.create_user_agents
        ])

    def get_drop_queries(self):
        DropQueries = namedtuple('DropQueries', [
            'drop_events',
            'drop_uploaded_files',
            'drop_pageviews',
            'drop_user_agents'
        ])

        return DropQueries._make([
            self.drop_events,
            self.drop_uploaded_files,
            self.drop_pageviews,
            self.drop_user_agents
        ])
