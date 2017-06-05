import yaml
import os
import sys
import boto3
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from queries import Queries
from parser import Parser
from event_parser import EventParser
from pageview_parser import PageViewParser
from database_connection import DataBaseConnection
from s3 import S3
from uploader import Uploader


def set_redshift_configs():
    # The bucket name and filename
    # could all be defined inside of the lambda resource in terraform.
    bucket = boto3.resource('s3').Bucket('tf-redshift-bucket-dev-secrets')
    data = yaml.load(bucket.Object('redshift_secrets.yml').get()['Body'])
    os.environ['redshift_user'] = data['redshift_user']
    os.environ['redshift_password'] = data['redshift_password']
    os.environ['redshift_host'] = data['redshift_host']

def lambda_handler(event, context):
    set_redshift_configs()
    if 'dest' in os.environ.keys():
        dest_bucket = "login-gov-{}-analytics".format(os.environ['env'])
    else:
        dest_bucket = 'tf-redshift-bucket-dev-analytics'

    if 'source' in os.environ.keys():
        source_bucket = "login-gov-{}-logs".format(os.environ['env'])
    else:
        source_bucket = 'login-gov-dev-logs'

    uploader = Uploader(source_bucket, dest_bucket, redshift=True)
    uploader.run()
