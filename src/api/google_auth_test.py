from google_auth import set_google_api_credentials, get_google_api_credentials
from gsc import ingest_gsc_data, ingest_pagespeed_data
from .logging_utils import get_logger

logger = get_logger(__name__)

MOCK_CREDS = {
    "client_id": "test-client-id",
    "client_secret": "test-client-secret",
    "access_token": "test-access-token",
    "refresh_token": "test-refresh-token"
}

def test_store_and_retrieve():
    logger.info("Storing mock credentials...")
    success = set_google_api_credentials(MOCK_CREDS)
    logger.info(f"Store success: {success}")
    logger.info("Retrieving credentials...")
    creds = get_google_api_credentials()
    logger.info(f"Retrieved credentials: {creds}")

def test_gsc_integration():
    logger.info("Testing ingest_gsc_data with no credentials passed...")
    result = ingest_gsc_data(site_url="https://example.com")
    logger.info(f"ingest_gsc_data result: {result}")
    logger.info("Testing ingest_pagespeed_data with no credentials passed...")
    result2 = ingest_pagespeed_data(url="https://example.com")
    logger.info(f"ingest_pagespeed_data result: {result2}")

if __name__ == "__main__":
    test_store_and_retrieve()
    test_gsc_integration() 