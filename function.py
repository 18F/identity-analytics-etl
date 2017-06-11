import yaml
import os
import sys
import boto3
import src


def set_redshift_configs():
    # The bucket name and filename
    # could all be defined inside of the lambda resource in terraform.
    bucket = boto3.resource('s3').Bucket('tf-redshift-bucket-dev-secrets')
    data = yaml.load(bucket.Object('redshift_secrets.yml').get()['Body'])
    os.environ['REDSHIFT_URI'] = "redshift+psycopg2://{redshift_user}:{redshift_password}@{redshift_host}:5432/analytics".format(
        redshift_user=data['redshift_user'],
        redshift_password=data['redshift_password'],
        redshift_host=data['redshift_host']
    )

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

    uploader = src.Uploader(source_bucket, dest_bucket, redshift=True)
    uploader.run()
