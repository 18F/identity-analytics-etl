import yaml
import os
import sys
import boto3
import src


# TODO: Seems the lambda_handler will run on every configured event and thus,
# invoke set_redshift_configs() on each run, maybe this should only be invoked once
# to set the variables in memory, this will prevent breaking in a case where a
# connection to the s3 bucket cannot be established.

def set_redshift_configs():
    # The bucket name and filename
    # could all be defined inside of the lambda resource in terraform.
    bucket = boto3.resource('s3').Bucket("tf-redshift-bucket-{}-secrets".format(os.environ.get('env')))
    data = yaml.load(bucket.Object('redshift_secrets.yml').get()['Body'])
    os.environ['REDSHIFT_URI'] = "redshift+psycopg2://awsuser:{redshift_password}@{redshift_host}:5439/analytics".format(
        redshift_password=data['redshift_password'],
        redshift_host=os.environ.get('redshift_host')
    )

def lambda_handler(event, context):
    set_redshift_configs()
    dest_bucket = "login-gov-{}-analytics".format(os.environ.get('env'))
    source_bucket = "login-gov-{}-logs".format(os.environ.get('env'))
    uploader = src.Uploader(source_bucket, dest_bucket, redshift=True)
    uploader.run()
