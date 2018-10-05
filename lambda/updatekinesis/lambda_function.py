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
    secret_dict = get_secret_dict(secrets_client, secret_name)
    # get delivery stream details
    firehose_dict = get_deliverystream_dict(firehose_client, delivery_stream_name)

    # update delivery stream
    try:
        firehose_client.update_destination(
            DeliveryStreamName = firehose_dict['DeliveryStreamName'],
            CurrentDeliveryStreamVersionId = firehose_dict['VersionId'],
            DestinationId = firehose_dict['Destinations'][0]['DestinationId'],
            RedshiftDestinationUpdate = {
                'Username': secret_dict['username'],
                'Password': secret_dict['password']
                }
            )
    except Exception as e:
        logger.error("Updating Kinesis Firehose failed with error {}".format(e))
        raise ValueError("Updating Kinesis Firehose %s failed." % (delivery_stream_name))

    return
    
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
        service_client (client): The kinesis service client

        streamname (string): The streamname

    Returns:
        DeliveryStreamDictionary: Delivery Stream dictionary

    Raises:
        ResourceNotFoundException: If the secret with the specified streamname does not exist

        ValueError: If the stream details is not valid JSON

    """
    
    try:
        deliverystream = service_client.describe_delivery_stream(DeliveryStreamName=streamname)
        deliverystream_dict = deliverystream['DeliveryStreamDescription']
    except Exception as e:
        logger.error("Failed to obtain firehose description with error {}".format(e))
        raise ValueError("Failed attempting to obtain firehose description for %s." % (streamname))
        
    return deliverystream_dict
    