import os
import psycopg2
from datetime import datetime

MIGRATIONS_DIR = os.path.dirname(os.path.abspath(__file__))
MIGRATIONS = [
    '001_add_tenants_and_cwv.sql',
]

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'jaffebot'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', 5432),
}

HISTORY_TABLE = 'migration_history'

def ensure_history_table(conn):
    with conn.cursor() as cur:
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {HISTORY_TABLE} (
                id SERIAL PRIMARY KEY,
                migration VARCHAR(255) NOT NULL,
                applied_at TIMESTAMP NOT NULL,
                applied_by VARCHAR(255) NOT NULL
            );
        ''')
    conn.commit()

def get_applied_migrations(conn):
    with conn.cursor() as cur:
        cur.execute(f"SELECT migration FROM {HISTORY_TABLE};")
        return set(row[0] for row in cur.fetchall())

def apply_migration(conn, migration_file):
    with open(os.path.join(MIGRATIONS_DIR, migration_file), 'r') as f:
        sql = f.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    with conn.cursor() as cur:
        cur.execute(f"""
            INSERT INTO {HISTORY_TABLE} (migration, applied_at, applied_by)
            VALUES (%s, %s, %s)
        """, (migration_file, datetime.utcnow(), os.getenv('USER', 'unknown')))
    conn.commit()

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    ensure_history_table(conn)
    applied = get_applied_migrations(conn)
    for migration in MIGRATIONS:
        if migration not in applied:
            print(f"Applying migration: {migration}")
            apply_migration(conn, migration)
        else:
            print(f"Already applied: {migration}")
    conn.close()

if __name__ == '__main__':
    main() 