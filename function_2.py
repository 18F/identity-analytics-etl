import src
import os
import yaml
import boto3
import logging

from secrets_manager import get_redshift_secrets


def set_redshift_configs(env, acct_id):
    redshift_prod_password = get_redshift_secrets(os.environ['env'])["password"]
    os.environ['REDSHIFT_URI'] = "redshift+psycopg2://awsuser:{redshift_password}@{redshift_host}/analytics".format(
        redshift_password=redshift_prod_password,
        redshift_host=os.environ['redshift_host']
    )
    os.environ['env'] = env

def lambda_handler(event, context):
    logging.getLogger().setLevel(logging.INFO)
    logging.info('function_2.py starting')

    os.environ['S3_USE_SIGV4'] = 'True'
    bucket = os.environ['hot_bucket']
    set_redshift_configs(os.environ['env'], os.environ['acct_id'])
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
                'events_email': ['id', 'name', 'domain_name', 'time'],
                'events_phone': ['id', 'visit_id', 'visitor_id', 'area_code','country_code','time']
               }
    s3 = src.S3(bucket, bucket, bucket, bucket, bucket, os.environ['encryption_key'])

    logging.info('s3.get_all_csv()')
    files = s3.get_all_csv()
    if len(files):
        logging.info("Found {} csv files to copy to Redshift".format(len(files)))
    else:
        logging.info("No csv files to copy to Redshift, exiting")
        return

    db = src.DataBaseConnection(redshift=True)
    db.build_db_if_needed()

    logging.info('Fetching list of all previously uploaded files')
    uploaded_files = db.uploaded_files()
    logging.info('Found {} previously uploaded files in Redshift'.format(
        len(uploaded_files)))

    success_counter = 0
    for f in files:
        if context.get_remaining_time_in_millis() < 10000:
            logging.error('Ran out of time in lambda, exiting!')
            break
        try:
            logging.info('Processing {!r}'.format(f))

            pth = "{}.txt".format('.'.join(f.split('.')[:-2]))
            table = f.split('.')[-2]

            logging.info('Checking if previously uploaded')
            if (pth, table) in uploaded_files:
                logging.info('File was previously uploaded, deleting it')
                s3.delete_from_bucket(f)
                continue

            logging.info('Loading CSV into Redshift -- db.load_csv()')

            db.load_csv(table,
                        pth,
                        s3.get_path(f),
                        headers[table],
                        os.environ['region'],
                        'arn:aws:iam::{}:role/tf-redshift-{}-iam-role'.format(
                        os.environ['acct_id'], os.environ['env']))

            logging.info('Finished copying to redshift, deleting from bucket')
            s3.delete_from_bucket(f)

            success_counter += 1
            logging.info('Done processing {!r}. Uploaded {} so far.'.format(
                f, success_counter))

        # TO-DO: Add granular/specific exception handling
        except Exception as e:
            logging.exception("Error while processing CSV file {}".format(e))
            s3.delete_from_bucket(f)

    db.close_connection()

    logging.info('Uploaded {} files this run out of {} pending'.format(
        success_counter, len(files)))
