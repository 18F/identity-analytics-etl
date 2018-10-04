import boto3
import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """ Updates the kinesis redshift firehose username and password
        with the current value from secretsmanager
    """
    
    secret_name = event['SecretName']
    delivery_stream_name = event['DeliveryStreamName']    

    # connect to secretsmanager
    secrets_client = boto3.client('secretsmanager', endpoint_url=os.environ['SECRETS_MANAGER_ENDPOINT'])
    # connect to firehose
    firehose_client = boto3.client('firehose')
    # get the current secret from secretsmanager
    current_dict = get_secret_dict(secrets_client, secret_name)
    # get delivery stream details
    kinesis_dict = get_deliverystream_dict(firehose_client, delivery_stream_name)


    # todo update delivery stream here
    DeliveryStreamName  = current_dict['DeliveryStreamName']
    CurrentDeliveryStreamVersionId  = kinesis_dict['VerisonId']
    DestinationId = kinesis_dict['Destinations'][0]['DestinationId']
    RedshiftDestinationUpdate={
        'Username': 'string',
        'Password': 'string'
    }
    
    return ''

def get_secret_dict(service_client, secretname):
    """Gets the secret dictionary corresponding for the secretname

    This helper function gets credentials for the secretname passed in and returns the dictionary by parsing the JSON string

    Args:
        service_client (client): The secrets manager service client

        secretname (string): The secretname or other identifier

    Returns:
        SecretDictionary: Secret dictionary

    Raises:
        ResourceNotFoundException: If the secret with the specified secretname and stage does not exist

        ValueError: If the secret is not valid JSON

        KeyError: If the secret json does not contain the expected keys

    """
    required_fields = ['username', 'password']

    secret = service_client.get_secret_value(SecretId=secretname, VersionStage='AWSCURRENT')
    plaintext = secret['SecretString']
    secret_dict = json.loads(plaintext)
    print (secret_dict)

    # Run validations against the secret
    for field in required_fields:
        if field not in secret_dict:
            raise KeyError("%s key is missing from secret JSON" % field)

    # Parse and return the secret JSON string
    return secret_dict
    
def get_deliverystream_dict(service_client, streamname):
    """Gets the delivery stream dictionary corresponding for the streamname

    This helper function gets stream details for the streamname passed in and returns the dictionary by parsing the JSON string

    Args:
        kinesis_client (client): The kinesis service client

        streamname (string): The streamname

    Returns:
        StreamDictionary: Stream dictionary

    Raises:
        ResourceNotFoundException: If the secret with the specified streamname does not exist

        ValueError: If the stream details is not valid JSON

    """
    
    # Parse and return the secret JSON string
    deliverystream = service_client.describe_delivery_stream(DeliveryStreamName=streamname)
    plaintext = deliverystream['DeliveryStreamDescription']
    deliverystream_dict = json.loads(plaintext)
    print (deliverystream_dict)

    return deliverystream_dict
    