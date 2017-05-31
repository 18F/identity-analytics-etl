import logging
import os

from event_parser import EventParser
from pageview_parser import PageViewParser
from database_connection import DataBaseConnection
from s3 import S3

class Uploader:

    def __init__(self, source_bucket, dest_bucket, s3=None, parsers=None, redshift=False):
        logging.basicConfig(level=logging.INFO)
        self.redshift = redshift
        self.db_conn = DataBaseConnection(redshift)
        self.source_bucket = source_bucket
        self.dest_bucket = dest_bucket
        self.s3 = S3(self.source_bucket, self.dest_bucket) if s3 is None else s3
        self.parsers = (EventParser(), PageViewParser()) if parsers is None else parsers
        self.logger = logging.getLogger('uploader')

    def run(self):
        self.db_conn.build_db_if_needed()
        self.s3.create_dest_bucket_if_not_exists()

        uploaded_files = self.db_conn.uploaded_files()
        logfiles = self.s3.get_s3_logfiles()

        self.logger.info("Total Files: {}".format(len(logfiles)))

        for f in logfiles:
            #TODO: make this validate table name as well
            if f in uploaded_files:
                continue

            self.logger.info("parsing {}".format(f))
            for parser in self.parsers:
                self.etl(parser, f)

    def etl(self, parser, logfile):
        csv_name = "{}.{}.csv".format(logfile.replace('.txt', ''), parser.table)
        in_file = self.s3.get_logfile(logfile)

        processed_rows, out = parser.stream_csv(in_file.read())
        if processed_rows > 0:
            self.s3.new_file(out, csv_name)
            self.db_conn.load_csv(parser.table,
                                  logfile,
                                  self.s3.get_path(csv_name),
                                  parser.headers,
                                  'us-west-2',
                                  'arn:aws:iam::555546682965:role/tf-redshift-iam-role')

        else:
            self.db_conn.mark_uploaded(logfile, parser.table)

        in_file.close()
        out.close()

if __name__ == '__main__':
    if 'env' in os.environ.keys():
        bucket = "login-gov-{}-analytics".format(os.environ['env'])
    else:
        bucket = 'tf-redshift-bucket-dev-analytics'

    uploader = Uploader('login-gov-prod-logs', bucket)
    uploader.run()
