import src
import os
import yaml
import sys
import boto3

from datetime import datetime, timedelta

def set_redshift_configs(env):
    # The bucket name and filename
    # could all be defined inside of the lambda resource in terraform.
    bucket = boto3.resource('s3').Bucket("login-gov-{}-redshift-secrets".format(env))
    data = yaml.load(bucket.Object('redshift_secrets.yml').get()['Body'])
    os.environ['REDSHIFT_URI'] = "redshift+psycopg2://awsuser:{redshift_password}@{redshift_host}/analytics".format(
        redshift_password=data['redshift_password'],
        redshift_host='tf-{}-redshift-cluster.ca6vppcizuju.us-west-2.redshift.amazonaws.com:5439'.format(env)
    )
    os.environ['env'] = env

if __name__ == '__main__':
    os.environ['S3_USE_SIGV4'] = 'True'
    bucket = 'login-gov-prod-analytics'
    set_redshift_configs('prod')
    headers = {'events': ['id', 'name', 'user_agent', 'user_id', 'user_ip',
                           'host', 'visit_id', 'visitor_id', 'time', 'event_properties',
                           'success', 'existing_user', 'otp_method', 'context',
                           'method', 'authn_context', 'service_provider', 'loa3',
                           'active_profile', 'errors'],
                'pageviews': ['method', 'path', 'format', 'controller', 'action',
                               'status', 'duration', 'user_id', 'user_agent', 'ip',
                               'host', 'uuid', 'timestamp'],
                'events_devices': ['id', 'name', 'user_agent', 'browser_name', 'browser_version',
                                   'browser_platform_name', 'browser_platform_version',
                                   'browser_device_name', 'browser_device_type', 'browser_bot', 'time'],
               }
    s3 = src.S3(bucket, 'login-gov-int-analytics', 'dc12706b-50ea-40b7-8d0e-206962aaa8f7')

    #uploader = src.Uploader('login-gov-int-logs', bucket, redshift=True)
    #uploader.run()
    files = s3.get_s3_logfiles_by_lookback(timedelta(hours=24))
    db = src.DataBaseConnection(redshift=True)
    uploaded_files = db.uploaded_files()

    for f in files:
        pth = "{}.txt".format('.'.join(f.split('.')[:-2]))
        table = f.split('.')[-2]
        if pth in uploaded_files:
            continue

        db.load_csv(table,
                    f,
                    s3.get_path(f),
                    headers[table],
                    'us-west-2',
                    'arn:aws:iam::555546682965:role/tf-redshift-{}-iam-role'.format(
                     os.environ.get('env')))
