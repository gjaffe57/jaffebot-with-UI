from .logging_utils import get_logger

logger = get_logger(__name__)

def monitor_redirects(urls: list, max_chain: int = 5) -> list:
    """
    Simulate monitoring HTTP redirects for a list of URLs.
    Args:
        urls (list): List of URLs to monitor.
        max_chain (int): Maximum allowed redirect chain length.
    Returns:
        list: Results with URL, redirect chain, and detected issues.
    """
    results = []
    for url in urls:
        # Mock: simulate a redirect chain
        chain = [url]
        for i in range(1, max_chain + 2):
            next_url = f"{url}/redirect{i}"
            chain.append(next_url)
            if i == max_chain:
                break
        issues = []
        if len(chain) > max_chain:
            issues.append("Redirect chain exceeds threshold")
        if len(set(chain)) < len(chain):
            issues.append("Infinite redirect loop detected")
        results.append({
            "url": url,
            "redirect_chain": chain,
            "issues": issues
        })
    return results

def monitor_uptime(urls: list, error_threshold: int = 2) -> list:
    """
    Simulate uptime monitoring for a list of URLs.
    Args:
        urls (list): List of URLs to monitor.
        error_threshold (int): Number of errors to flag as persistent.
    Returns:
        list: Results with URL, status history, and detected issues.
    """
    results = []
    for url in urls:
        # Mock: simulate a status history
        status_history = [200, 200, 500, 404, 200, 503]
        errors = [code for code in status_history if code >= 400]
        issues = []
        if len(errors) > error_threshold:
            issues.append("Persistent errors detected")
        if 503 in status_history:
            issues.append("Downtime detected")
        results.append({
            "url": url,
            "status_history": status_history,
            "issues": issues
        })
    return results

def aggregate_and_format_alerts(redirect_results: list, uptime_results: list) -> list:
    """
    Aggregate and format alerts from redirect and uptime monitoring results.
    Args:
        redirect_results (list): Results from monitor_redirects.
        uptime_results (list): Results from monitor_uptime.
    Returns:
        list: Alert payloads with URL, issue type, severity, and details.
    """
    alerts = []
    url_issues = {}
    # Aggregate redirect issues
    for r in redirect_results:
        if r["issues"]:
            url_issues.setdefault(r["url"], []).extend([("redirect", issue) for issue in r["issues"]])
    # Aggregate uptime issues
    for u in uptime_results:
        if u["issues"]:
            url_issues.setdefault(u["url"], []).extend([("uptime", issue) for issue in u["issues"]])
    # Format alerts
    for url, issues in url_issues.items():
        for issue_type, detail in issues:
            severity = "critical" if "downtime" in detail.lower() or "exceeds" in detail.lower() else "warning"
            alerts.append({
                "url": url,
                "issue_type": issue_type,
                "severity": severity,
                "detail": detail
            })
    return alerts

def deploy_monitoring_agent(urls: list) -> list:
    """
    Simulate integrating and deploying the monitoring agent.
    Args:
        urls (list): List of URLs to monitor.
    Returns:
        list: Aggregated alerts from the monitoring workflow.
    """
    logger.info("Starting monitoring agent deployment...")
    redirect_results = monitor_redirects(urls)
    uptime_results = monitor_uptime(urls)
    alerts = aggregate_and_format_alerts(redirect_results, uptime_results)
    logger.info(f"Monitoring complete. {len(alerts)} alerts generated.")
    return alerts 