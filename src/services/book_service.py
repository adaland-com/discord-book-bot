from typing import Optional, List, Dict, Any
import requests

from src.clients.open_library import (
    search_books,
    convert_to_book_data,
    BookData,
)
from src.parsers.book_parser import (
    build_search_query,
)
from src.services.logging_service import log_search_attempt


def search_open_library(
    session: requests.Session,
    title: Optional[str] = None,
    author: Optional[str] = None
) -> Optional[BookData]:

    log_search_attempt("Open Library", title, author)
    
    query = build_search_query(title, author)
    
    if not query:
        return None
    
    result = search_books(session, query, limit=5)
    
    if result and result.get('books'):
        ol_book = result['books'][0]
        return convert_to_book_data(session, ol_book)
    
    return None


def search_book(
    session: requests.Session,
    title: Optional[str] = None,
    author: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    result = search_open_library(session, title, author)
    if result:
        return _book_data_to_dict(result)
    
    return None


def _book_data_to_dict(book_data: BookData) -> Dict[str, Any]:
    return {
        'title': book_data.title,
        'author': book_data.author,
        'rating': book_data.rating,
        'description': book_data.description,
        'cover_url': book_data.cover_url,
        'publication_year': book_data.publication_year,
        'url': book_data.url,
        'source': book_data.source,
        'goodreads_url': book_data.goodreads_url,
    }


def validate_search_params(
    title: Optional[str],
    author: Optional[str]
) -> tuple[bool, Optional[str]]:
    if not title and not author:
        return False, "Please provide at least a title or an author!"
    return True, None
