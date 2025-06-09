-- Migration: 001_add_tenants_and_cwv.sql
-- Description: Adds multi-tenant support and enhances CWV monitoring
-- Author: JaffeBot Team
-- Date: 2024-03-21

-- Start transaction
BEGIN;

-- Create tenants table
CREATE TABLE IF NOT EXISTS tenants (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_tenant_name UNIQUE (name)
);

-- Add tenant_id to existing tables
ALTER TABLE search_analytics 
    ADD COLUMN IF NOT EXISTS tenant_id INTEGER REFERENCES tenants(id);

ALTER TABLE coverage 
    ADD COLUMN IF NOT EXISTS tenant_id INTEGER REFERENCES tenants(id);

ALTER TABLE performance 
    ADD COLUMN IF NOT EXISTS tenant_id INTEGER REFERENCES tenants(id);

ALTER TABLE pagespeed 
    ADD COLUMN IF NOT EXISTS tenant_id INTEGER REFERENCES tenants(id);

-- Add CWV metrics to pagespeed table
ALTER TABLE pagespeed
    ADD COLUMN IF NOT EXISTS ttfb FLOAT, -- Time to First Byte
    ADD COLUMN IF NOT EXISTS fcp FLOAT, -- First Contentful Paint
    ADD COLUMN IF NOT EXISTS tti FLOAT, -- Time to Interactive
    ADD COLUMN IF NOT EXISTS tbt FLOAT; -- Total Blocking Time

-- Add indexes for tenant-based queries
CREATE INDEX IF NOT EXISTS idx_search_analytics_tenant 
    ON search_analytics(tenant_id);

CREATE INDEX IF NOT EXISTS idx_coverage_tenant 
    ON coverage(tenant_id);

CREATE INDEX IF NOT EXISTS idx_performance_tenant 
    ON performance(tenant_id);

CREATE INDEX IF NOT EXISTS idx_pagespeed_tenant 
    ON pagespeed(tenant_id);

-- Add index for tenant name lookups
CREATE INDEX IF NOT EXISTS idx_tenants_name 
    ON tenants(name);

-- Add trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tenants_updated_at
    BEFORE UPDATE ON tenants
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Commit transaction
COMMIT;

-- Rollback script (for reference)
/*
BEGIN;

-- Drop triggers
DROP TRIGGER IF EXISTS update_tenants_updated_at ON tenants;
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Drop indexes
DROP INDEX IF EXISTS idx_tenants_name;
DROP INDEX IF EXISTS idx_pagespeed_tenant;
DROP INDEX IF EXISTS idx_performance_tenant;
DROP INDEX IF EXISTS idx_coverage_tenant;
DROP INDEX IF EXISTS idx_search_analytics_tenant;

-- Drop tenant_id columns
ALTER TABLE pagespeed DROP COLUMN IF EXISTS tenant_id;
ALTER TABLE performance DROP COLUMN IF EXISTS tenant_id;
ALTER TABLE coverage DROP COLUMN IF EXISTS tenant_id;
ALTER TABLE search_analytics DROP COLUMN IF EXISTS tenant_id;

-- Drop CWV columns
ALTER TABLE pagespeed 
    DROP COLUMN IF EXISTS ttfb,
    DROP COLUMN IF EXISTS fcp,
    DROP COLUMN IF EXISTS tti,
    DROP COLUMN IF EXISTS tbt;

-- Drop tenants table
DROP TABLE IF EXISTS tenants;

COMMIT;
*/ 