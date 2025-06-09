import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_robots_txt(domain: str) -> str:
    url = urljoin(domain, '/robots.txt')
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text

def fetch_sitemap_xml(domain: str) -> list:
    url = urljoin(domain, '/sitemap.xml')
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')]
    return urls

def fetch_llms_txt(domain: str) -> list:
    url = urljoin(domain, '/LLMs.txt')
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        return []
    # Assume each line is a URL or resource
    urls = [line.strip() for line in resp.text.splitlines() if line.strip()]
    return urls

def aggregate_urls(domain: str) -> dict:
    robots = fetch_robots_txt(domain)
    sitemap_urls = fetch_sitemap_xml(domain)
    llms_urls = fetch_llms_txt(domain)
    # Optionally, parse robots.txt for Disallow/Allow URLs (not implemented here)
    all_urls = set(sitemap_urls + llms_urls)
    return {
        'robots_txt': robots,
        'sitemap_urls': sitemap_urls,
        'llms_urls': llms_urls,
        'all_urls': list(all_urls)
    } 