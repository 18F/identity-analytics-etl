import os
import pytz
import logging
from datetime import datetime, timedelta
import random

from .event_parser import EventParser
from .pageview_parser import PageViewParser
from .device_parser import DeviceParser
from .email_parser import EmailParser
from .phone_parser import PhoneParser
from .database_connection import DataBaseConnection
from .s3 import S3


class Uploader:

    def __init__(self, source_bucket, dest_bucket, dest_bucket_parquet, hot_bucket, staging_bucket, logger=None, s3=None, parsers=None, redshift=False, encryption_key="b10a84ce-1f80-44bc-8d0f-7a547b45ce53", lookback_period=None, staging_stream_rate=10):
        self.redshift = redshift
        self.source_bucket = source_bucket
        self.dest_bucket = dest_bucket
        self.dest_bucket_parquet = dest_bucket_parquet
        self.hot_bucket = hot_bucket
        self.staging_bucket = staging_bucket
        self.staging_stream_rate = staging_stream_rate
        self.s3 = S3(self.source_bucket, self.dest_bucket, self.dest_bucket_parquet, self.hot_bucket, self.staging_bucket, encryption_key) if s3 is None else s3
        self.parsers = (EventParser(), PageViewParser(), DeviceParser(), EmailParser(), PhoneParser()) if parsers is None else parsers
        if not logger:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger('uploader')
        else:
            self.logger = logger
        self.lookback_period = 20 if lookback_period is None else lookback_period

    def run(self, trigger_file=None):
        if trigger_file:
            logfiles = [trigger_file]
        else:
            logfiles = self.s3.get_s3_logfiles_by_lookback(timedelta(hours=self.lookback_period))

        self.logger.info("Total Files: {}".format(len(logfiles)))
        self.logger.info(logfiles)
        for f in logfiles:
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
        parquet_name = "{}/{}.snappy.parquet".format(parser.table, logfile.replace('.txt', ''))
        in_file = self.s3.get_logfile(logfile)

        processed_rows, out, out_parquet = parser.stream_csv(in_file.read())

        if processed_rows > 0:
            self.s3.new_file(out, csv_name)
            self.s3.new_file_parquet(out_parquet, parquet_name)
            self.s3.new_file_hot(out, csv_name)

        # Copy ~ X% files as-is to staging bucket.
        if random.randint(1,100) <= self.staging_stream_rate:
            self.s3.new_file_staging(self.s3.get_logfile(logfile), logfile)

        in_file.close()
        out.close()
