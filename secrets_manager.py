# This package manages secrets for the analytics-etl using AWS Secrets Manager
# Secrets are stored(encrypted at rest) into AWS and decrypted at runtime using AWS KMS

import json
import boto3
from botocore.exceptions import ClientError
import logging

def get_redshift_secrets(env,region="us-west-2"):
    ''' returns a dict-like representation of Redshift's secret profile(key/values) with host,port, url
        username, password, etc. AWS provides either a string or binary representation.'''

    secret_name =  "{}/redshift/lambda_hot".format(env)
    endpoint_url = "https://secretsmanager.{}.amazonaws.com".format(region)
    session = boto3.session.Session()
    client = session.client(
        service_name = 'secretsmanager',
        region_name  = region,
        endpoint_url=endpoint_url
    )
    
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId = secret_name
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            logging.exception("The request secret profile {} was not found".format(secret_name))
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            logging.exception("The Request was invalid due to {}".format(e))
        elif e.response["Error"]["Code"] == "InvalidParamentException":
            logging.exception("The request has invalid parameters {}".format(e))
        raise
    
    else:
        # Decrypted secret using the associated KMS Key(Analytics-<env>-Key)
        # The secret profile is a string, but can add logic for binary('SecretBinary') if needed
        return json.loads(get_secret_value_response['SecretString'])

