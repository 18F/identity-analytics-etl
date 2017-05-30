import sqlalchemy as sql

from datetime import datetime
from queries import Queries

class DataBaseConnection:
    q = Queries()

    def __init__(self, redshift=False):
        self.redshift = redshift
        if not redshift:
            self.engine = sql.create_engine('postgresql://localhost/dev')
        else:
            # How to connect to Redshift using IAM roles + Name?
            self.engine = sql.create_engine('')

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
        header = 'IGNOREHEADER 1' if self.redshift else 'HEADER'
        columns = '"' + '", "'.join(columns) + '"'
        
        if self.redshift:
            self.connection.execute(self.q.load_csv_redshift.format(table,
                columns, csv_path, iam_role, region, header))
        else:
            self.connection.execute(self.q.load_csv.format(table, columns,
                csv_path, header))

        self.mark_uploaded(filename, table)

    def drop_tables(self):
        for query in self.q.get_drop_queries()._asdict().values():
            self.connection.execute(query)

    def close_connection(self):
        self.connection.close()
