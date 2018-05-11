import yaml
import os
import sys
import boto3
import logging
import src

def set_redshift_configs():
    # The bucket name and filename
    # could all be defined inside of the lambda resource in terraform.
    bucket = boto3.resource('s3').Bucket("login-gov-{}-{}-redshift-secrets".format(os.environ.get('env'), os.environ.get('acct_id')))
    data = yaml.load(bucket.Object('redshift_secrets.yml').get()['Body'])
    os.environ['REDSHIFT_URI'] = "redshift+psycopg2://awsuser:{redshift_password}@{redshift_host}/analytics".format(
        redshift_password=data['redshift_password'],
        redshift_host=os.environ.get('redshift_host')
    )

def lambda_handler(event, context):
    logging.basicConfig(level=logging.INFO)
    uploader_logger = logging.getLogger('uploader')
    set_redshift_configs()
    trigger_file = event["Records"][0]["s3"]["object"]["key"]
    dest_bucket = os.environ.get('dest_bucket')
    source_bucket = os.environ.get('source_bucket')
    bucket_parquet = os.environ.get('bucket_parquet')
    hot_bucket = os.environ.get('hot_bucket')

    uploader = src.Uploader(
        source_bucket,
        dest_bucket,
        bucket_parquet,
        hot_bucket,
        logger=uploader_logger,
        redshift=True,
        encryption_key=os.environ.get('encryption_key'),
    )

    uploader.run(trigger_file=trigger_file)
