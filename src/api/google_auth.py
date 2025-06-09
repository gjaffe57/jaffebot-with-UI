from . import aws_secrets
from typing import Optional
from .logging_utils import get_logger

logger = get_logger(__name__)

SECRET_NAME = "google-oauth2-tokens"

def get_google_api_credentials() -> Optional[dict]:
    """
    Retrieve OAuth 2.0 credentials (access and refresh tokens) from AWS Secrets Manager.
    Returns:
        dict or None: Credentials if found, else None.
    """
    creds = aws_secrets.get_secret(SECRET_NAME)
    if creds:
        return creds
    else:
        logger.warning(f"No credentials found in AWS Secrets Manager under '{SECRET_NAME}'.")
        return None

def set_google_api_credentials(credentials: dict) -> bool:
    """
    Store OAuth 2.0 credentials (access and refresh tokens) in AWS Secrets Manager.
    Args:
        credentials (dict): The credentials to store.
    Returns:
        bool: True if successful, False otherwise.
    """
    return aws_secrets.put_secret(SECRET_NAME, credentials)

def get_google_api_credentials_old():
    """
    Set up OAuth 2.0 authentication for Google APIs (GSC, PageSpeed).
    Steps:
    1. Register your application in Google Cloud Console to obtain client_id and client_secret.
    2. Download the OAuth 2.0 credentials JSON file.
    3. Use google-auth and google-auth-oauthlib to perform the OAuth flow.
    4. Store the access and refresh tokens securely (e.g., in a file or database).
    5. Use the credentials to authenticate API requests.

    Returns:
        dict: Mock credentials (replace with real credentials in production).
    """
    # Placeholder for real OAuth flow
    # Example: credentials = google.oauth2.credentials.Credentials(...)
    return {
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "access_token": "MOCK_ACCESS_TOKEN",
        "refresh_token": "MOCK_REFRESH_TOKEN"
    } 