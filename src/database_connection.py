import sqlalchemy as sql

from datetime import datetime
from .queries import Queries

class DataBaseConnection:
    q = Queries()

    def __init__(self):
        self.engine = sql.create_engine('postgresql://localhost/dev')
        self.connection = engine.connect()

    def build_db_if_needed(self):
        if not self.engine.dialect.has_table(self.engine, 'uploaded_files'):
            for query in self.q.get_build_queries()._as_dict().values():
                self.connection.execute(query)

    def uploaded_files(self):
        return self.connection.execute(self.q.get_uploaded_files)

    def mark_uploaded(self, filename, destination):
        # Do I really need destination here?
        uploaded_at = datetime.now()
        self.connection.execute(self.q.mark_uploaded.format(filename,
            destination,
            uploaded_at))

    def load_csv(self, table, filename, csv_path, columns, region, iam_role, redshift=True):
        header = 'IGNOREHEADER 1' if redshift else 'HEADER'

        if redshift:
            self.connection.execute(self.q.load_csv_redshift.format(table,
                columns, csv_path, iam_role, region, header)
        else:
            self.connection.execute(self.q.load_csv.format(table, columns,
                csv_path, header))

        self.mark_uploaded(filename, table)

    def drop_tables(self):
        for query in self.q.get_drop_queries()._as_dict().values():
            self.connection.execute(query)

    def close_connection(self):
        self.connection.close()
