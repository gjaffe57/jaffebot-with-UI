"""
Celery Configuration for JaffeBot Agents

- Broker: RabbitMQ (amqp://guest:guest@localhost:5672//)
- No backend is configured (set to None)
- Micro-agent queues: discovery, audit, content, backlink
- Each agent task is assigned to its own queue
- Retry strategy: autoretry for all exceptions, exponential backoff, max 3 retries
- Error handling: logs errors using Celery's task logger

To add new agents, define a new queue and corresponding @celery_app.task with the desired configuration.
"""
from celery import Celery
from celery.utils.log import get_task_logger
import os
import openai
from celery.schedules import crontab
from .logging_utils import setup_logging, get_logger
import logging

celery_app = Celery(
    "jaffebot_agents",
    broker="amqp://guest:guest@localhost:5672//",
    backend=None
)

# Set up logging with PII redaction
setup_logging(
    level=logging.INFO,
    format_str='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_file='logs/celery.log'
)

logger = get_logger(__name__)

# Define queues for micro-agents
celery_app.conf.task_queues = (
    {
        "name": "discovery",
    },
    {
        "name": "audit",
    },
    {
        "name": "content",
    },
    {
        "name": "backlink",
    },
)

# Periodic task: Automate content refresh every hour
celery_app.conf.beat_schedule = {
    'automate-content-refresh': {
        'task': 'src.api.celery_app.automate_content_refresh',
        'schedule': crontab(minute=0, hour='*'),  # every hour
    },
}

@celery_app.task(queue="discovery", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def discovery_task():
    try:
        logger.info("Discovery agent task executed")
        return "Discovery agent task executed"
    except Exception as e:
        logger.error(f"Discovery agent error: {e}")
        raise

@celery_app.task(queue="audit", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def audit_task():
    try:
        logger.info("Audit agent task executed")
        return "Audit agent task executed"
    except Exception as e:
        logger.error(f"Audit agent error: {e}")
        raise

@celery_app.task(queue="content", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def content_task():
    try:
        logger.info("Content agent task executed")
        return "Content agent task executed"
    except Exception as e:
        logger.error(f"Content agent error: {e}")
        raise

@celery_app.task(queue="backlink", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def backlink_task():
    try:
        logger.info("Backlink agent task executed")
        return "Backlink agent task executed"
    except Exception as e:
        logger.error(f"Backlink agent error: {e}")
        raise

@celery_app.task(queue="content", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def openai_content_suggestion(prompt: str):
    """
    Generate content suggestions using the OpenAI API.
    Args:
        prompt (str): The prompt or topic for content suggestion.
    Returns:
        str: The generated content suggestion from OpenAI.
    """
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            logger.error("OPENAI_API_KEY not set in environment.")
            return "API key missing."
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256
        )
        suggestion = response.choices[0].message["content"].strip()
        logger.info(f"OpenAI content suggestion generated for prompt: {prompt}")
        return suggestion
    except Exception as e:
        logger.error(f"OpenAI content suggestion error: {e}")
        raise

@celery_app.task(queue="content", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def update_content_task(url: str, new_content: str):
    """
    Simulate updating content at the given URL with new content.
    Args:
        url (str): The URL of the page to update.
        new_content (str): The new content to apply.
    Returns:
        str: Success message indicating the update.
    """
    try:
        logger.info(f"Updating content at {url} with new content: {new_content[:60]}...")
        # Simulate update (in real implementation, this would push to CMS or database)
        return f"Content at {url} updated successfully."
    except Exception as e:
        logger.error(f"Content update error for {url}: {e}")
        raise

@celery_app.task(queue="content", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def monitor_content_update(url: str, status: str, feedback: str = ""):
    """
    Monitor the result of a content update and collect feedback.
    Args:
        url (str): The URL of the updated content.
        status (str): The result status (e.g., 'success', 'failure').
        feedback (str, optional): Additional feedback or comments.
    Returns:
        str: Summary message of the monitoring event.
    """
    try:
        logger.info(f"Monitoring content update for {url}: status={status}, feedback={feedback}")
        # In a real implementation, this could store results in a database or send notifications
        return f"Monitoring complete for {url}: status={status}, feedback={feedback}"
    except Exception as e:
        logger.error(f"Monitoring error for {url}: {e}")
        raise

@celery_app.task
def add(x, y):
    return x + y

@celery_app.task(name='src.api.celery_app.automate_content_refresh')
def automate_content_refresh():
    """
    Periodic task to automate content refresh for a list of URLs.
    - Runs every hour (configurable via Celery beat)
    - For each URL, generates a content suggestion and updates the content
    - Logs the automation process
    """
    try:
        # Mocked list of URLs to refresh
        urls = [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3"
        ]
        for url in urls:
            prompt = f"Suggest updated content for {url}"
            suggestion = openai_content_suggestion.apply(args=(prompt,)).get()
            update_content_task.apply(args=(url, suggestion))
            logger.info(f"Automated content refresh for {url} completed.")
        return f"Automated content refresh completed for {len(urls)} URLs."
    except Exception as e:
        logger.error(f"Automated content refresh error: {e}")
        raise 