import psycopg2
import os
import boto3
from botocore.exceptions import NoRegionError
from .logging_utils import setup_logging, get_logger
import logging

# Set up logging with PII redaction
setup_logging(
    level=logging.INFO,
    format_str='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_file='logs/app.log',
    json_format=True
)

# Get logger for this module
logger = get_logger(__name__)

def create_tenant(conn, name: str) -> int:
    """
    Create a new tenant and return its ID.
    """
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO tenants (name) VALUES (%s) RETURNING id;
        """, (name,))
        tenant_id = cur.fetchone()[0]
    conn.commit()
    logger.info(f"Created tenant '{name}' with id {tenant_id}")
    return tenant_id

def get_tenant_id(conn, name: str) -> int:
    """
    Get tenant ID by name.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM tenants WHERE name = %s;", (name,))
        result = cur.fetchone()
        return result[0] if result else None

def store_search_analytics(conn, analytics: list, site_url: str, tenant_id: int):
    """
    Store search analytics data in the DB for a tenant.
    """
    with conn.cursor() as cur:
        for row in analytics:
            logger.info(f"Inserting search_analytics for {site_url} (tenant {tenant_id}): {row}")
            cur.execute("""
                INSERT INTO search_analytics (site_url, query, clicks, impressions, ctr, position, tenant_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                site_url, row['query'], row.get('clicks'), row.get('impressions'),
                row.get('ctr'), row.get('position'), tenant_id
            ))
    conn.commit()

def store_coverage(conn, coverage: dict, site_url: str, tenant_id: int):
    """
    Store coverage data in the DB for a tenant.
    """
    with conn.cursor() as cur:
        logger.info(f"Inserting coverage for {site_url} (tenant {tenant_id}): {coverage}")
        cur.execute("""
            INSERT INTO coverage (site_url, valid, error, excluded, tenant_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            site_url, coverage.get('valid'), coverage.get('error'), coverage.get('excluded'), tenant_id
        ))
    conn.commit()

def store_performance(conn, performance: dict, site_url: str, tenant_id: int):
    """
    Store performance data in the DB for a tenant.
    """
    with conn.cursor() as cur:
        logger.info(f"Inserting performance for {site_url} (tenant {tenant_id}): {performance}")
        cur.execute("""
            INSERT INTO performance (site_url, average_position, total_clicks, total_impressions, tenant_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            site_url, performance.get('average_position'), performance.get('total_clicks'),
            performance.get('total_impressions'), tenant_id
        ))
    conn.commit()

def store_pagespeed(conn, pagespeed: dict, tenant_id: int) -> int:
    """
    Store pagespeed data in the DB for a tenant and return inserted id.
    Supports new CWV fields.
    """
    with conn.cursor() as cur:
        logger.info(f"Inserting pagespeed for {pagespeed['url']} (tenant {tenant_id}): {pagespeed}")
        cur.execute("""
            INSERT INTO pagespeed (
                url, lcp, fid, cls, score, ttfb, fcp, tti, tbt, tenant_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            pagespeed['url'], pagespeed.get('lcp'), pagespeed.get('fid'), pagespeed.get('cls'),
            pagespeed.get('score'), pagespeed.get('ttfb'), pagespeed.get('fcp'),
            pagespeed.get('tti'), pagespeed.get('tbt'), tenant_id
        ))
        pagespeed_id = cur.fetchone()[0]
    conn.commit()
    return pagespeed_id

def store_pagespeed_opportunities(conn, opportunities: list, pagespeed_id: int):
    """
    Store pagespeed opportunities in the DB.
    """
    with conn.cursor() as cur:
        for opp in opportunities:
            logger.info(f"Inserting pagespeed_opportunity for pagespeed_id {pagespeed_id}: {opp}")
            cur.execute("""
                INSERT INTO pagespeed_opportunities (pagespeed_id, name, savings)
                VALUES (%s, %s, %s)
            """, (
                pagespeed_id, opp.get('name'), opp.get('savings')
            ))
    conn.commit()

def get_secrets_client():
    try:
        return boto3.client('secretsmanager')
    except NoRegionError:
        # Fallback to a default region, but log a warning
        logger.warning("AWS region not set. Falling back to 'us-east-1'.")
        return boto3.client('secretsmanager', region_name='us-east-1')

# Log messages with PII will be automatically redacted
logger.info("User email: john.doe@example.com")  # Will be redacted
logger.error("API key: sk-1234567890")  # Will be redacted 