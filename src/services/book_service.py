from typing import Optional
import logging
import requests

from config import SEARCH

from src.clients.open_library import (
    search_books,
    convert_to_book_data,
    BookData,
    build_search_query,
)

logger = logging.getLogger(__name__)


def search_open_library(
    session: requests.Session,
    title: Optional[str] = None,
    author: Optional[str] = None
) -> Optional[BookData]:
    query_parts = []
    if title:
        query_parts.append(f"title: {title}")
    if author:
        query_parts.append(f"author: {author}")
    query_str = " | ".join(query_parts) if query_parts else "empty query"
    logger.info(f"[Open Library] Searching: {query_str}")
    
    query = build_search_query(title, author)
    
    if not query:
        return None
    
    result = search_books(session, query, limit=SEARCH.max_results)
    
    if result and result.get('books'):
        ol_book = result['books'][0]
        return convert_to_book_data(session, ol_book)
    
    return None


def validate_search_params(
    title: Optional[str],
    author: Optional[str]
) -> tuple[bool, Optional[str]]:
    if not title and not author:
        return False, "Please provide at least a title or an author!"
    return True, None
