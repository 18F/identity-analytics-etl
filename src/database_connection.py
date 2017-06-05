import os

import sqlalchemy as sql

from datetime import datetime
from queries import Queries

class DataBaseConnection:
    q = Queries()

    def __init__(self, redshift=False):
        """
        Connects by default to local postgresql. This should eventually default
        to redshift
        """

        self.redshift = redshift
        if not redshift:
            self.engine = sql.create_engine('postgresql://localhost/dev')
        else:
            # How to connect to Redshift using IAM roles + Name?
            self.engine = sql.create_engine(
                "redshift+psycopg2://{redshift_user}:{redshift_password}@{redshift_host}:5432/analytics".format(
                    redshift_user=os.environ['redshift_user'],
                    redshift_password=os.environ['redshift_password'],
                    redshift_host=os.environ['redshift_host']
                )
            )

        self.connection = self.engine.connect()

    def build_db_if_needed(self):
        if not self.engine.dialect.has_table(self.engine, 'uploaded_files'):
            for query in self.q.get_build_queries()._asdict().values():
                self.connection.execute(query)

    def uploaded_files(self):
        result = self.connection.execute(self.q.get_uploaded_files)
        return [row['s3filename'] for row in result]

    def mark_uploaded(self, filename, destination):
        uploaded_at = datetime.now()
        self.connection.execute(self.q.mark_uploaded.format(filename,
            destination,
            uploaded_at))

    def load_csv(self, table, filename, csv_path, columns, region, iam_role):
        if self.redshift:
            self.connection.execute(self.q.get_load_csv_redshift(table,
                columns, csv_path, iam_role, region))
        else:
            # TODO: Make this run for Postgres + s3 bucket, get file, format file path , etc
            self.connection.execute(self.q.get_load_csv(table, columns, csv_path))

        self.mark_uploaded(filename, table)

    def drop_tables(self):
        for query in self.q.get_drop_queries()._asdict().values():
            self.connection.execute(query)

    def close_connection(self):
        self.connection.close()
