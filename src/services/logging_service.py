"""Pure functions for logging."""
import datetime
from typing import Optional


def format_log_message(
    user_name: str,
    command: str,
    query: Optional[str] = None,
    location: str = "Unknown"
) -> str:
    """Format a log message for bot usage."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if query:
        return f"[{timestamp}] {user_name} used {command} | Query: '{query}' | Location: {location}"
    return f"[{timestamp}] {user_name} used {command} | Location: {location}"


def log_usage(
    user_name: str,
    command: str,
    query: Optional[str] = None,
    location: str = "Unknown"
) -> None:
    """Log bot usage to console."""
    message = format_log_message(user_name, command, query, location)
    print(message)


def log_search_attempt(
    source: str,
    title: Optional[str] = None,
    author: Optional[str] = None
) -> None:
    """Log a search attempt from a specific source."""
    query_parts = []
    if title:
        query_parts.append(f"title: {title}")
    if author:
        query_parts.append(f"author: {author}")
    
    query_str = " | ".join(query_parts) if query_parts else "empty query"
    print(f"[{source}] Searching: {query_str}")
