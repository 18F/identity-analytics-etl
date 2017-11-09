import os

import sqlalchemy as sql
import psycopg2

from datetime import datetime
from .queries import Queries


class DataBaseConnection:
    q = Queries()
    # TODO: use a seperate DB for tests? add test DB?

    def __init__(self, s3=None, redshift=False):
        """
        Connects by default to local postgresql.
        """

        self.redshift = redshift
        self.s3 = s3
        if not redshift:
            self.engine = sql.create_engine('postgresql://localhost/dev')
        else:
            self.engine = sql.create_engine(
                            os.environ.get('REDSHIFT_URI'),
                            connect_args={'sslmode': 'verify-ca'}
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
        self.connection.execute(self.q.mark_uploaded.format(
                                    filename,
                                    destination,
                                    uploaded_at
                                )
                               )

    def load_csv(self, table, filename, csv_path, columns, region, iam_role):
        if self.redshift:
            self.connection.execute(self.q.get_load_csv_redshift(table,
                columns, csv_path, iam_role, region))
        else:
            if 's3' in csv_path:
                path = csv_path.split('/')[-1]
                self.s3.download_file(path)
                self.connection.execute(
                                            self.q.get_load_csv(
                                                table,
                                                columns,
                                                "/tmp/{}".format(path)
                                            )
                                        )
                os.remove("/tmp/{}".format(path))
            else:
                self.connection.execute(self.q.get_load_csv(table, columns, csv_path))

        self.mark_uploaded(filename, table)

    def drop_tables(self):
        for query in self.q.get_drop_queries()._asdict().values():
            self.connection.execute(query)

    def close_connection(self):
        self.connection.close()
