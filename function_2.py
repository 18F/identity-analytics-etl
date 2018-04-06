import src
import os
import yaml
import boto3

def set_redshift_configs(env):
    bucket = boto3.resource('s3').Bucket("login-gov-{}-redshift-secrets".format(env))
    data = yaml.load(bucket.Object('redshift_secrets.yml').get()['Body'])
    os.environ['REDSHIFT_URI'] = "redshift+psycopg2://awsuser:{redshift_password}@{redshift_host}/analytics".format(
        redshift_password=data['redshift_password'],
        redshift_host='tf-{}-redshift-cluster.ca6vppcizuju.us-west-2.redshift.amazonaws.com:5439'.format(env)
    )
    os.environ['env'] = env

def lambda_handler(event, context):
    os.environ['S3_USE_SIGV4'] = 'True'
    bucket = 'login-gov-{}-analytics-hot'.format(os.environ.get('env'))
    set_redshift_configs(os.environ.get('env'))
    headers = {'events': ['id', 'name', 'user_agent', 'user_id', 'user_ip',
                           'host', 'visit_id', 'visitor_id', 'time', 'event_properties',
                           'success', 'existing_user', 'otp_method', 'context',
                           'method', 'authn_context', 'service_provider', 'loa3',
                           'active_profile', 'errors'],
                'pageviews': ['method', 'path', 'format', 'controller', 'action',
                               'status', 'duration', 'user_id', 'user_agent', 'ip',
                               'host', 'uuid', 'timestamp'],
                'events_devices': ['id', 'name', 'user_agent', 'browser_name',
                                   'browser_version', 'browser_platform_name',
                                   'browser_platform_version', 'browser_device_name',
                                   'browser_device_type', 'browser_bot', 'time'],
                'events_email': ['id', 'name', 'domain_name', 'time']
               }
    s3 = src.S3(bucket, bucket, bucket, bucket, 'dc12706b-50ea-40b7-8d0e-206962aaa8f7')

    files = s3.get_all_csv()
    db = src.DataBaseConnection(redshift=True)
    db.build_db_if_needed()
    uploaded_files = db.uploaded_files()

    for f in files:
        if context.get_remaining_time_in_millis() < 1000:
            break

        pth = "{}.txt".format('.'.join(f.split('.')[:-2]))
        table = f.split('.')[-2]
        if (pth, table) in uploaded_files:
            s3.delete_from_bucket(f)
            continue

        db.load_csv(table,
                    pth,
                    s3.get_path(f),
                    headers[table],
                    'us-west-2',
                    'arn:aws:iam::555546682965:role/tf-redshift-{}-iam-role'.format(
                     os.environ.get('env')))
        s3.delete_from_bucket(f)

    db.close_connection()
