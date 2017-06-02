import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from queries import Queries
from parser import Parser
from event_parser import EventParser
from pageview_parser import PageViewParser
from database_connection import DataBaseConnection
from s3 import S3
from uploader import Uploader


def lambda_handler(event, context):
    if 'dest' in os.environ.keys():
        dest_bucket = "login-gov-{}-analytics".format(os.environ['env'])
    else:
        dest_bucket = 'tf-redshift-bucket-dev-analytics'

    if 'source' in os.environ.keys():
        source_bucket = "login-gov-{}-logs".format(os.environ['env'])
    else:
        source_bucket = 'login-gov-dev-logs'

    uploader = Uploader(source_bucket, dest_bucket)
    uploader.run()
