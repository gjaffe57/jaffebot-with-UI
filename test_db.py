import psycopg2
from psycopg2 import sql, IntegrityError

conn = psycopg2.connect(dbname='your_db', user='your_user', password='your_pass', host='localhost')
conn.autocommit = True
cur = conn.cursor()

def run(query, params=None):
    cur.execute(query, params or ())
    return cur

def assert_rowcount(expected):
    assert cur.rowcount == expected, f'Expected {expected} rows, got {cur.rowcount}'

try:
    # Clean tables
    run('TRUNCATE domains, users, crawls, crawl_urls, gsc_metrics, audit_results, audit_issues, backlinks, outreach RESTART IDENTITY CASCADE;')

    # Insert domain and user
    run('INSERT INTO domains (name) VALUES (%s);', ('example.com',))
    run('INSERT INTO users (email, name) VALUES (%s, %s);', ('admin@example.com', 'Admin User'))

    # Insert crawl event
    run('INSERT INTO crawls (domain_id, user_id, agent) VALUES (1, 1, %s);', ('DiscoveryAgent',))

    # Insert crawl URL
    run('INSERT INTO crawl_urls (crawl_id, url, status_code) VALUES (1, %s, %s);', ('https://example.com/', 200))

    # Insert GSC metrics
    run('INSERT INTO gsc_metrics (domain_id, url, date, clicks, impressions, ctr, position) VALUES (1, %s, %s, %s, %s, %s, %s);', ('https://example.com/', '2024-06-01', 100, 1000, 0.1, 1.5))

    # Insert audit result and issue
    run('INSERT INTO audit_results (crawl_url_id, audit_type, score, summary) VALUES (1, %s, %s, %s);', ('indexability', 95.0, 'Noindex tag not found.'))
    run('INSERT INTO audit_issues (audit_result_id, issue_type, description, severity, recommendation) VALUES (1, %s, %s, %s, %s);', ('indexability', 'Noindex tag missing', 'medium', 'Add a noindex tag.'))

    # Insert backlink and outreach
    run('INSERT INTO backlinks (domain_id, url, source_url, anchor_text) VALUES (1, %s, %s, %s);', ('https://example.com/', 'https://referrer.com/', 'Example Anchor'))
    run('INSERT INTO outreach (backlink_id, contact_email, status, notes) VALUES (1, %s, %s, %s);', ('webmaster@referrer.com', 'sent', 'Initial outreach sent.'))

    # Update and delete
    run('UPDATE domains SET name = %s WHERE id = 1;', ('updated.com',))
    run('DELETE FROM outreach WHERE id = 1;')

    # Constraint checks
    try:
        run('INSERT INTO domains (name) VALUES (%s);', ('updated.com',))  # duplicate name
    except IntegrityError:
        print('Passed: Duplicate domain name rejected')
        conn.rollback()
    try:
        run('INSERT INTO crawls (domain_id) VALUES (%s);', (999,))  # invalid domain_id
    except IntegrityError:
        print('Passed: Invalid domain_id rejected')
        conn.rollback()

    # Query and assert
    cur.execute('SELECT COUNT(*) FROM domains;')
    assert cur.fetchone()[0] == 1
    cur.execute('SELECT COUNT(*) FROM users;')
    assert cur.fetchone()[0] == 1
    print('All tests passed!')
finally:
    cur.close()
    conn.close() 