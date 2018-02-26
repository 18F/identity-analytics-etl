import os
import pytz
import logging
from datetime import datetime, timedelta

from .event_parser import EventParser
from .pageview_parser import PageViewParser
from .device_parser import DeviceParser
from .database_connection import DataBaseConnection
from .s3 import S3


class Uploader:

    def __init__(self, source_bucket, dest_bucket, dest_bucket_parquet, logger=None, s3=None, parsers=None, redshift=False, encryption_key="dc12706b-50ea-40b7-8d0e-206962aaa8f7", trigger_file=None, lookback_period=None):
        self.redshift = redshift
        self.source_bucket = source_bucket
        self.dest_bucket = dest_bucket
        self.dest_bucket_parquet = dest_bucket_parquet
        self.s3 = S3(self.source_bucket, self.dest_bucket, self.dest_bucket_parquet, encryption_key) if s3 is None else s3
        self.db_conn = DataBaseConnection(self.s3, redshift)
        self.parsers = (EventParser(), PageViewParser(), DeviceParser()) if parsers is None else parsers
        if not logger:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger('uploader')
        else:
            self.logger = logger
        self.trigger_file = trigger_file
        self.lookback_period = 20 if lookback_period is None else lookback_period

    def run(self):
        self.db_conn.build_db_if_needed()

        uploaded_files = self.db_conn.uploaded_files()

        if self.trigger_file:
            logfiles = [self.trigger_file]
        else:
            logfiles = self.s3.get_s3_logfiles_by_lookback(timedelta(hours=self.lookback_period))

        self.logger.info("Total Files: {}".format(len(logfiles)))
        self.logger.info(logfiles)
        for f in logfiles:
            if f in uploaded_files:
                continue

            self.logger.info("parsing {}".format(f))
            for parser in self.parsers:
                try:
                    self.etl(parser, f)
                except:
                    self.logger.error("An Error occurred parsing {}".format(f))
                    print("An Error occurred parsing {}".format(f))
                    raise


    def etl(self, parser, logfile):
        csv_name = "{}.{}.csv".format(logfile.replace('.txt', ''), parser.table)
        parquet_name = "{}/{}.parquet.gz".format(parser.table, logfile.replace('.txt', ''))
        in_file = self.s3.get_logfile(logfile)

        processed_rows, out, out_parquet = parser.stream_csv(in_file.read())

        if processed_rows > 0:
            self.s3.new_file(out, csv_name)
            self.s3.new_file_parquet(out_parquet, parquet_name)
            self.db_conn.load_csv(parser.table,
                                  logfile,
                                  self.s3.get_path(csv_name),
                                  parser.headers,
                                  'us-west-2',
                                  'arn:aws:iam::555546682965:role/tf-redshift-{}-iam-role'.format(
                                    os.environ.get('env')
                                  ))

        else:
            self.db_conn.mark_uploaded(logfile, parser.table)

        in_file.close()
        out.close()
