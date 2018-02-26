import os
import unittest

from context import Uploader
from fake_s3 import FakeS3


class UploaderTestCases(unittest.TestCase):

    def test_uploader(self):
        _s3 = FakeS3('source', 'dest')
        uploader = Uploader('source', 'dest', 'dest-parquet', s3=_s3)
        uploader.db_conn.drop_tables()
        uploader.run()


if __name__ == '__main__':
    unittest.main()
