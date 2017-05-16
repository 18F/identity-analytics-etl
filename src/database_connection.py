from .queries import Queries

class DataBaseConnection:
    q = Queries()

    def __init__(self):
        # create connection here ?
        pass

    def build_db_if_needed(self):
        # add check query to run here
        pass

    def uploaded_files(self):
        # run query to get file names
        pass

    def mark_uploaded(self, filename):
        pass

    def load_csv(self, filename, csv_path, columns, region, iam_role, redshift)
        pass
