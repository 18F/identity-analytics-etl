import src
import os
import yaml
import sys
import boto3

def set_redshift_configs(env):
    # The bucket name and filename
    # could all be defined inside of the lambda resource in terraform.
    bucket = boto3.resource('s3').Bucket("login-gov-{}-redshift-secrets".format(env))
    data = yaml.load(bucket.Object('redshift_secrets.yml').get()['Body'])
    os.environ['REDSHIFT_URI'] = "redshift+psycopg2://awsuser:{redshift_password}@{redshift_host}/analytics".format(
        redshift_password=data['redshift_password'],
        redshift_host='tf-int-redshift-cluster.ca6vppcizuju.us-west-2.redshift.amazonaws.com:5439'
    )
    os.environ['env'] = env

if __name__ == '__main__':
    os.environ['S3_USE_SIGV4'] = 'True'
    if 'env' in os.environ.keys():
        bucket = "login-gov-{}-analytics".format(os.environ['env'])
        bucket_parquet = "login-gov-{}-analytics-parquet".format(os.environ['env'])
    else:
        bucket = 'login-gov-int-analytics'
        bucket_parquet = 'login-gov-int-analytics-parquet'

    set_redshift_configs(os.environ['env'])

    uploader = src.Uploader('login-gov-int-logs', bucket, bucket_parquet, redshift=True)
    uploader.run()
