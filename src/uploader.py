import logging

from .event_parser import EventParser
from .pageview_parser import PageViewParser
from .database_connection import DataBasConnection

class Uploader:

    def __init__(self, source_bucket, dest_bucket, s3=None, parsers=None):
        self.source_bucket = source_bucket
        self.dest_bucket = dest_bucket
        self.s3 = s3
        self.parsers = (EventParser(), PageViewParser()) if parsers is None else parsers

    def run(self):
        pass

    def get_s3_logfiles(self):
        pass

    def get_database_connection(self):
        pass

    def get_s3(self):
        pass

    def etl(parser, logfile):
        pass
