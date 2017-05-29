import unittest
import sys
import os
import io
sys.path.insert(0, 'src/')

from s3 import S3


class S3TestCases(unittest.TestCase):
    s3 = S3('tf-redshift-bucket-dev-source', 'tf-redshift-bucket-dev-dest')

    def setup(self):
        with open('test.txt', 'w') as f:
            f.write('test')

        self.s3.source_bucket.upload_file('test.txt', 'test.txt')
        os.remove('test.txt')

    def test_get_logfiles(self):
        self.setup()
        res = self.s3.get_s3_logfiles()
        self.assertTrue('test.txt' in res)

    def test_get_logfile(self):
        self.setup()
        res = self.s3.get_logfile('test.txt')
        self.assertEqual(res.read().decode('utf-8'), 'test')

    def test_new_file(self):
        out = io.StringIO('This is a test')
        self.s3.new_file(out, 'new_file.txt')
        res = self.s3.dest_bucket.Object('new_file.txt').get()['Body'].read().decode('utf-8')
        self.assertEqual(res, 'This is a test')


if __name__ == '__main__':
    unittest.main()
