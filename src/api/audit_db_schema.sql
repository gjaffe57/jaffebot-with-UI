-- Audit DB Schema for GSC and PageSpeed Data

-- Table: search_analytics
CREATE TABLE search_analytics (
    id SERIAL PRIMARY KEY,
    site_url TEXT NOT NULL,
    query TEXT NOT NULL,
    clicks INTEGER,
    impressions INTEGER,
    ctr FLOAT,
    position FLOAT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: coverage
CREATE TABLE coverage (
    id SERIAL PRIMARY KEY,
    site_url TEXT NOT NULL,
    valid INTEGER,
    error INTEGER,
    excluded INTEGER,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: performance
CREATE TABLE performance (
    id SERIAL PRIMARY KEY,
    site_url TEXT NOT NULL,
    average_position FLOAT,
    total_clicks INTEGER,
    total_impressions INTEGER,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: pagespeed
CREATE TABLE pagespeed (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    lcp FLOAT, -- Largest Contentful Paint (seconds)
    fid INTEGER, -- First Input Delay (ms)
    cls FLOAT, -- Cumulative Layout Shift
    score INTEGER, -- Performance score
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: pagespeed_opportunities
CREATE TABLE pagespeed_opportunities (
    id SERIAL PRIMARY KEY,
    pagespeed_id INTEGER REFERENCES pagespeed(id),
    name TEXT,
    savings TEXT
); 