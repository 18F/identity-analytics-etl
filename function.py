import yaml
import os
import sys
import boto3
import logging

def load_additional_deps():
    import zipfile
    print('Loading from zip:')
    cwd = os.getcwd()
    os.chdir('/tmp')
    filename = 'dependencies.zip'
    zip_file_path = filename
    bucket = boto3.resource('s3').Bucket("login-gov-analytics-dependencies")
    # download addl deps from s3, and put them into /tmp
    bucket.download_file(filename, zip_file_path)
    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall()
    zip_ref.close()
    print('Result: ')
    print(os.listdir(os.getcwd()))
    os.chdir(cwd)

load_additional_deps()

import src

def set_redshift_configs():
    # The bucket name and filename
    # could all be defined inside of the lambda resource in terraform.
    bucket = boto3.resource('s3').Bucket("login-gov-{}-redshift-secrets".format(os.environ.get('env')))
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
    dest_bucket = "login-gov-{}-analytics".format(os.environ.get('env'))
    source_bucket = "login-gov-{}-logs".format(os.environ.get('env'))
    bucket_parquet = "login-gov-{}-analytics-parquet".format(os.environ['env'])

    uploader = src.Uploader(
        source_bucket,
        dest_bucket,
        bucket_parquet,
        logger=uploader_logger,
        redshift=True,
        encryption_key=os.environ.get('encryption_key'),
        trigger_file=trigger_file
    )

    uploader.run()
