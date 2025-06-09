import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from .discovery import aggregate_urls
from .gsc import fetch_gsc_data

def check_indexability(domain: str, path: str = "/") -> dict:
    url = urljoin(domain, path)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    meta_robots = soup.find("meta", attrs={"name": "robots"})
    robots_content = meta_robots["content"] if meta_robots and meta_robots.has_attr("content") else None
    return {
        "url": url,
        "meta_robots": robots_content,
        "indexable": robots_content is None or "noindex" not in robots_content.lower()
    }

def check_core_web_vitals(domain: str, path: str = "/") -> dict:
    # Placeholder: Real Core Web Vitals require field data or Lighthouse/CrUX API
    return {
        "url": urljoin(domain, path),
        "core_web_vitals": "Not implemented (requires external API or browser)"
    }

def check_schema_markup(domain: str, path: str = "/") -> dict:
    url = urljoin(domain, path)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    schemas = []
    # JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            schemas.append(json.loads(script.string))
        except Exception:
            pass
    # Microdata and RDFa (simplified)
    microdata = soup.find_all(attrs={"itemscope": True})
    rdfa = soup.find_all(attrs={"typeof": True})
    return {
        "url": url,
        "json_ld": schemas,
        "microdata_count": len(microdata),
        "rdfa_count": len(rdfa)
    }

def check_mobile_friendly(domain: str, path: str = "/") -> dict:
    url = urljoin(domain, path)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    meta_viewport = soup.find("meta", attrs={"name": "viewport"})
    mobile_friendly = meta_viewport is not None
    return {
        "url": url,
        "mobile_friendly": mobile_friendly,
        "viewport": meta_viewport["content"] if mobile_friendly else None
    }

def correlate_metrics_and_generate_issues(domain: str) -> list:
    """
    Correlate technical checks and GSC data for all discovered URLs and generate a JSON list of issues.
    Args:
        domain (str): The domain to audit.
    Returns:
        list: List of issue dicts for each URL.
    """
    try:
        url_data = aggregate_urls(domain)
        urls = url_data.get('all_urls', [])
        gsc_data = fetch_gsc_data(domain)
        issues = []
        for url in urls:
            if not url.startswith("http"):
                url = urljoin(domain, url)
            idx = check_indexability(url)
            vitals = check_core_web_vitals(url)
            schema = check_schema_markup(url)
            mobile = check_mobile_friendly(url)
            url_issues = {
                'url': url,
                'indexable': idx.get('indexable'),
                'meta_robots': idx.get('meta_robots'),
                'core_web_vitals': vitals.get('core_web_vitals'),
                'schema_json_ld': schema.get('json_ld'),
                'microdata_count': schema.get('microdata_count'),
                'rdfa_count': schema.get('rdfa_count'),
                'mobile_friendly': mobile.get('mobile_friendly'),
                'viewport': mobile.get('viewport'),
                'gsc_impressions': gsc_data.get('impressions'),
                'gsc_clicks': gsc_data.get('clicks'),
                'gsc_ctr': gsc_data.get('ctr'),
                'issues': []
            }
            if not idx.get('indexable'):
                url_issues['issues'].append('Not indexable')
            if not schema.get('json_ld') and schema.get('microdata_count', 0) == 0 and schema.get('rdfa_count', 0) == 0:
                url_issues['issues'].append('No schema markup detected')
            if not mobile.get('mobile_friendly'):
                url_issues['issues'].append('Not mobile-friendly')
            if gsc_data.get('impressions', 0) < 100:
                url_issues['issues'].append('Low impressions')
            if gsc_data.get('clicks', 0) < 10:
                url_issues['issues'].append('Low clicks')
            issues.append(url_issues)
        return issues
    except Exception as e:
        return [{"error": str(e)}]

def generate_markdown_report(issues: list) -> str:
    """
    Generate a Markdown report from the JSON issue list.
    Args:
        issues (list): List of issue dicts for each URL.
    Returns:
        str: Markdown-formatted report.
    """
    try:
        md = ["# Audit Report\n"]
        for issue in issues:
            md.append(f"## {issue.get('url')}")
            md.append("| Metric | Value |\n|---|---|")
            md.append(f"| Indexable | {issue.get('indexable')} |")
            md.append(f"| Meta Robots | {issue.get('meta_robots')} |")
            md.append(f"| Core Web Vitals | {issue.get('core_web_vitals')} |")
            md.append(f"| Schema JSON-LD | {bool(issue.get('schema_json_ld'))} |")
            md.append(f"| Microdata Count | {issue.get('microdata_count')} |")
            md.append(f"| RDFa Count | {issue.get('rdfa_count')} |")
            md.append(f"| Mobile Friendly | {issue.get('mobile_friendly')} |")
            md.append(f"| Viewport | {issue.get('viewport')} |")
            md.append(f"| GSC Impressions | {issue.get('gsc_impressions')} |")
            md.append(f"| GSC Clicks | {issue.get('gsc_clicks')} |")
            md.append(f"| GSC CTR | {issue.get('gsc_ctr')} |")
            if issue.get('issues'):
                md.append(f"\n**Issues:** {', '.join(issue.get('issues'))}\n")
            md.append("\n")
        return "\n".join(md)
    except Exception as e:
        return f"Error generating Markdown report: {e}"

def generate_html_report(issues: list) -> str:
    """
    Generate an HTML report from the JSON issue list.
    Args:
        issues (list): List of issue dicts for each URL.
    Returns:
        str: HTML-formatted report.
    """
    try:
        html = ["<html><head><title>Audit Report</title><style>table{border-collapse:collapse;}th,td{border:1px solid #ccc;padding:4px;}th{background:#eee;}</style></head><body>"]
        html.append("<h1>Audit Report</h1>")
        for issue in issues:
            html.append(f"<h2>{issue.get('url')}</h2>")
            html.append("<table>")
            html.append("<tr><th>Metric</th><th>Value</th></tr>")
            html.append(f"<tr><td>Indexable</td><td>{issue.get('indexable')}</td></tr>")
            html.append(f"<tr><td>Meta Robots</td><td>{issue.get('meta_robots')}</td></tr>")
            html.append(f"<tr><td>Core Web Vitals</td><td>{issue.get('core_web_vitals')}</td></tr>")
            html.append(f"<tr><td>Schema JSON-LD</td><td>{bool(issue.get('schema_json_ld'))}</td></tr>")
            html.append(f"<tr><td>Microdata Count</td><td>{issue.get('microdata_count')}</td></tr>")
            html.append(f"<tr><td>RDFa Count</td><td>{issue.get('rdfa_count')}</td></tr>")
            html.append(f"<tr><td>Mobile Friendly</td><td>{issue.get('mobile_friendly')}</td></tr>")
            html.append(f"<tr><td>Viewport</td><td>{issue.get('viewport')}</td></tr>")
            html.append(f"<tr><td>GSC Impressions</td><td>{issue.get('gsc_impressions')}</td></tr>")
            html.append(f"<tr><td>GSC Clicks</td><td>{issue.get('gsc_clicks')}</td></tr>")
            html.append(f"<tr><td>GSC CTR</td><td>{issue.get('gsc_ctr')}</td></tr>")
            html.append("</table>")
            if issue.get('issues'):
                html.append(f"<p><strong>Issues:</strong> {', '.join(issue.get('issues'))}</p>")
        html.append("</body></html>")
        return "\n".join(html)
    except Exception as e:
        return f"<p>Error generating HTML report: {e}</p>" 