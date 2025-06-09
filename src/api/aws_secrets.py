import boto3
import json
from botocore.exceptions import ClientError, NoRegionError
from typing import Optional
from .logging_utils import get_logger

logger = get_logger(__name__)

def get_secrets_client():
    try:
        return boto3.client('secretsmanager')
    except NoRegionError:
        logger.warning("AWS region not set. Falling back to 'us-east-1'.")
        return boto3.client('secretsmanager', region_name='us-east-1')

def get_secret(secret_name: str) -> Optional[dict]:
    """
    Retrieve a secret from AWS Secrets Manager and return it as a dict.
    Args:
        secret_name (str): The name of the secret in AWS Secrets Manager.
    Returns:
        dict or None: The secret value as a dictionary, or None if not found.
    """
    secrets_client = get_secrets_client()
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        secret = response.get('SecretString')
        if secret:
            return json.loads(secret)
    except ClientError as e:
        logger.error(f"Error retrieving secret {secret_name}: {e}")
    return None

def put_secret(secret_name: str, secret_value: dict) -> bool:
    """
    Store or update a secret in AWS Secrets Manager.
    Args:
        secret_name (str): The name of the secret in AWS Secrets Manager.
        secret_value (dict): The secret value to store (will be JSON-encoded).
    Returns:
        bool: True if successful, False otherwise.
    """
    secrets_client = get_secrets_client()
    try:
        # Try to update the secret if it exists
        secrets_client.put_secret_value(SecretId=secret_name, SecretString=json.dumps(secret_value))
        return True
    except secrets_client.exceptions.ResourceNotFoundException:
        # If the secret doesn't exist, create it
        try:
            secrets_client.create_secret(Name=secret_name, SecretString=json.dumps(secret_value))
            return True
        except ClientError as e:
            logger.error(f"Error creating secret {secret_name}: {e}")
    except ClientError as e:
        logger.error(f"Error updating secret {secret_name}: {e}")
    return False 