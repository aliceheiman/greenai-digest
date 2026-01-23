"""Background scheduler for article fetching.

This module handles scheduled article fetching using APScheduler.
It can be easily replaced with GitHub Actions or other scheduling mechanisms
by simply not importing this module in main.py.
"""

import logging
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


def create_scheduler(fetch_function, hour=2, minute=0):
    """
    Create and start a background scheduler for article fetching.

    Args:
        fetch_function: Callable that fetches articles
        hour: Hour in UTC (0-23) to run the job
        minute: Minute (0-59) to run the job

    Returns:
        BackgroundScheduler instance (already started)
    """
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        func=fetch_function,
        trigger="cron",
        hour=hour,
        minute=minute,
        id="fetch_articles",
        name="Fetch RSS articles nightly",
        misfire_grace_time=3600,  # Allow 1 hour grace period if missed
    )
    scheduler.start()
    logger.info(
        f"🕐 Scheduler started - articles will be fetched daily at {hour:02d}:{minute:02d} UTC"
    )
    return scheduler
