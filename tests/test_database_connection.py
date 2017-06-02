import unittest
import sys
import csv
import os


from context import DataBaseConnection
from context import Queries


class DataBaseTestCases(unittest.TestCase):
    columns = ['method', 'path', 'ip', 'timestamp']

    def setup(self):
        db_conn = DataBaseConnection()
        db_conn.drop_tables()
        db_conn.build_db_if_needed()
        return db_conn

    def csv_upload(self):
        db_conn = self.setup()
        with open("{}/fixtures/test_csv.csv".format(os.path.dirname(os.path.realpath(__file__))), 'w') as out:
            writer = csv.writer(out, delimiter=',')
            writer.writerow(self.columns)
            writer.writerow(['GET', '/', '127.0.0.1', '2017-04-10 17:45:22'])

        db_conn.load_csv('pageviews',
                         'test_csv.csv',
                         "{}/fixtures/test_csv.csv".format(os.path.dirname(os.path.realpath(__file__))),
                         self.columns,
                         'us-west-2',
                         'arn:aws:iam::555546682965:role/tf-redshift-iam-role')

        return db_conn

    def test_uploaded_files(self):
        db_conn = self.setup()
        db_conn.mark_uploaded('a.txt', 'test')
        self.assertTrue('a.txt' in db_conn.uploaded_files())

    def test_not_in_uploaded_files(self):
        db_conn = self.setup()
        db_conn.mark_uploaded('a.txt', 'test')
        self.assertFalse('b.txt' in db_conn.uploaded_files())

    def test_csv_upload(self):
        db_conn = self.csv_upload()
        self.assertTrue('test_csv.csv' in db_conn.uploaded_files())

    def test_csv_upload_values(self):
        db_conn = self.csv_upload()
        result = db_conn.connection.execute("SELECT * FROM pageviews;")
        self.assertEqual(result.first()['method'], 'GET')


if __name__ == '__main__':
    unittest.main()
