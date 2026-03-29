import logging
from typing import Optional


logger = logging.getLogger(__name__)


def format_log_message(
    user_name: str,
    command: str,
    query: Optional[str] = None,
    location: str = "Unknown"
) -> str:
    if query:
        return f"{user_name} used {command} | Query: '{query}' | Location: {location}"
    return f"{user_name} used {command} | Location: {location}"


def log_usage(
    user_name: str,
    command: str,
    query: Optional[str] = None,
    location: str = "Unknown"
) -> None:
    message = format_log_message(user_name, command, query, location)
    logger.info(message)


def log_search_attempt(
    source: str,
    title: Optional[str] = None,
    author: Optional[str] = None
) -> None:
    query_parts = []
    if title:
        query_parts.append(f"title: {title}")
    if author:
        query_parts.append(f"author: {author}")
    
    query_str = " | ".join(query_parts) if query_parts else "empty query"
    logger.info(f"[{source}] Searching: {query_str}")
