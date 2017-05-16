import sqlalchemy as sql

from datetime import datetime
from .queries import Queries

class DataBaseConnection:
    q = Queries()

    def __init__(self):
        self.engine = sql.create_engine('postgresql://{}'.format)
        self.connection = engine.connect()

    def build_db_if_needed(self):
        # There is definitely a better way to handle this
        if not self.engine.dialect.has_table(self.engine, 'uploaded_files'):
            for query in self.q.get_build_queries()._as_dict().values():
                self.connection.execute(query)

    def uploaded_files(self):
        # why do I need destination here?
        return self.connection.execute(self.q.get_uploaded_files)

    def mark_uploaded(self, filename):
        # Do I really need destination here?
        uploaded_at = datetime.now()
        self.connection.execute(self.q.mark_uploaded.format(filename, uploaded_at))

    def load_csv(self, filename, csv_path, columns, region, iam_role, redshift):
        # Call mark uploaded
        pass

    def drop_tables(self):
        for query in self.q.get_drop_queries()._as_dict().values():
            self.connection.execute(query)

    def close_connection(self):
        self.connection.close()
