import yaml
import os
import sys
import boto3
import logging
import src
import random

def set_redshift_configs():
    # The bucket name and filename
    # could all be defined inside of the lambda resource in terraform.
    bucket = boto3.resource('s3').Bucket("login-gov-{}-{}-redshift-secrets".format(os.environ['env'], os.environ['acct_id']))
    data = yaml.load(bucket.Object('redshift_secrets.yml').get()['Body'])
    os.environ['REDSHIFT_URI'] = "redshift+psycopg2://awsuser:{redshift_password}@{redshift_host}/analytics".format(
        redshift_password=data['redshift_password'],
        redshift_host=os.environ['redshift_host']
    )

def lambda_handler(event, context):
    logging.basicConfig(level=logging.INFO)
    uploader_logger = logging.getLogger('uploader')
    set_redshift_configs()
    trigger_file = event['Records'][0]['s3']['object']['key']
    dest_bucket = os.environ['dest_bucket']
    source_bucket = os.environ['source_bucket']
    staging_bucket = os.environ['staging_bucket']
    parquet_bucket = os.environ['parquet_bucket']
    hot_bucket = os.environ['hot_bucket']
    
    uploader = src.Uploader(
        source_bucket,
        dest_bucket,
        parquet_bucket,
        hot_bucket,
        staging_bucket,
        logger=uploader_logger,
        redshift=True,
        encryption_key=os.environ['encryption_key']
    )

    uploader.run(trigger_file=trigger_file)
