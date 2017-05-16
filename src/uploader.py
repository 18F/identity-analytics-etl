import logging
import boto

from .event_parser import EventParser
from .pageview_parser import PageViewParser
from .database_connection import DataBaseConnection

class Uploader:
    db_conn = DataBaseConnection()

    def __init__(self, source_bucket, dest_bucket, s3=None, parsers=None):
        self.source_bucket = source_bucket
        self.dest_bucket = dest_bucket
        self.s3 = s3
        self.parsers = (EventParser(), PageViewParser()) if parsers is None else parsers

    def run(self):
        db_conn.build_db_if_needed()
        uploaded_files = db_conn.uploaded_files()

        logging.info("Total Files: {}".format(len(self.get_s3_logfiles())))

        for f in self.get_s3_logfiles():
            if f in uploaded_files:
                continue

            for parser in self.parsers:
                self.etl(parser, f)

    def get_s3_logfiles(self):
        files = []

        conn = self.get_s3()
        bucket = conn.get_bucket(self.source_bucket)

        for f in bucket.list():
            if '.txt' in f:
                files.append(f)

        return files

    def get_s3(self):
        if self.s3:
            return self.s3
        else:
            # May Need Connect_to_region here to leverage IAM roles
            return boto.connect_s3()

    def etl(parser, logfile):
        csv_name = "{}.{}".format(logfile, parser.table)
        conn = self.get_s3()

        in_file = conn.get_bucket(self.source_bucket).Object(logfile)

        processed_rows = parser.stream_csv(in_file, csv_name)
        if processed_rows > 0:
            bucket = conn.get_bucket(self.dest_bucket)
            k = bucket.new_key(csv_name)
            k.set_contents_from_filename(csv_name)

            self.db_conn.load_csv(# add here)
        else:
            self.db_conn.mark_uploaded(logfile)
