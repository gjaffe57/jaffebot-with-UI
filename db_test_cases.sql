-- db_test_cases.sql: Manual validation for SEO audit database schema

-- Insert sample domain and user
tRUNCATE domains, users, crawls, crawl_urls, gsc_metrics, audit_results, audit_issues, backlinks, outreach RESTART IDENTITY CASCADE;
INSERT INTO domains (name) VALUES ('example.com');
INSERT INTO users (email, name) VALUES ('admin@example.com', 'Admin User');

-- Insert crawl event
INSERT INTO crawls (domain_id, user_id, agent) VALUES (1, 1, 'DiscoveryAgent');

-- Insert crawl URL
INSERT INTO crawl_urls (crawl_id, url, status_code) VALUES (1, 'https://example.com/', 200);

-- Insert GSC metrics
INSERT INTO gsc_metrics (domain_id, url, date, clicks, impressions, ctr, position) VALUES (1, 'https://example.com/', '2024-06-01', 100, 1000, 0.1, 1.5);

-- Insert audit result and issue
INSERT INTO audit_results (crawl_url_id, audit_type, score, summary) VALUES (1, 'indexability', 95.0, 'Noindex tag not found.');
INSERT INTO audit_issues (audit_result_id, issue_type, description, severity, recommendation) VALUES (1, 'indexability', 'Noindex tag missing', 'medium', 'Add a noindex tag.');

-- Insert backlink and outreach
INSERT INTO backlinks (domain_id, url, source_url, anchor_text) VALUES (1, 'https://example.com/', 'https://referrer.com/', 'Example Anchor');
INSERT INTO outreach (backlink_id, contact_email, status, notes) VALUES (1, 'webmaster@referrer.com', 'sent', 'Initial outreach sent.');

-- Update and delete tests
UPDATE domains SET name = 'updated.com' WHERE id = 1;
DELETE FROM outreach WHERE id = 1;

-- Constraint checks (should fail)
-- Uncomment to test: INSERT INTO domains (name) VALUES ('updated.com'); -- duplicate name
-- Uncomment to test: INSERT INTO crawls (domain_id) VALUES (999); -- invalid domain_id

-- Index usage (EXPLAIN)
EXPLAIN SELECT * FROM gsc_metrics WHERE domain_id = 1 AND url = 'https://example.com/' AND date = '2024-06-01';
EXPLAIN SELECT * FROM audit_results WHERE crawl_url_id = 1; 