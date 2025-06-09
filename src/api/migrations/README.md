# Database Migrations

This directory contains database migration files for the JaffeBot 3.0 project.

## Migration Files

### 001_add_tenants_and_cwv.sql
- Adds multi-tenant support with a new `tenants` table
- Adds tenant context to all existing tables
- Enhances Core Web Vitals (CWV) monitoring
- Adds appropriate indexes for performance
- Includes rollback functionality

## Usage

To apply migrations:

1. Ensure you have the correct database credentials
2. Run the migration:
   ```bash
   psql -U <username> -d <database> -f 001_add_tenants_and_cwv.sql
   ```

To rollback:
1. Uncomment the rollback section at the bottom of the migration file
2. Run the rollback commands

## Best Practices

1. Always test migrations in a development environment first
2. Take a database backup before applying migrations
3. Run migrations during low-traffic periods
4. Monitor the application after migration
5. Keep track of applied migrations in a separate table

## Migration Status

| Migration | Applied | Applied At | Applied By |
|-----------|---------|------------|------------|
| 001       | No      | -          | -          | 