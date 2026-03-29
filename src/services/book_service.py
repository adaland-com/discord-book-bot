"""Pure functions for book search operations."""
from typing import Optional, List, Dict, Any
import requests

from src.clients.open_library import (
    search_books,
    convert_to_book_data,
    BookData,
    create_session,
)
from src.parsers.book_parser import (
    build_search_query,
    translate_polish_title,
    author_matches,
)
from src.services.logging_service import log_search_attempt


def search_open_library(
    session: requests.Session,
    title: Optional[str] = None,
    author: Optional[str] = None
) -> Optional[BookData]:
    """
    Search for a book using Open Library API.
    
    Tries multiple strategies:
    1. Direct search with provided title/author
    2. Polish to English title translation if needed
    3. Broader author-only search as fallback
    
    Returns BookData if found, None otherwise.
    """
    log_search_attempt("Open Library", title, author)
    
    # Build and execute search query
    query = build_search_query(title, author)
    
    if not query:
        return None
    
    # Try Polish language first, then English, then any
    for language in ['pol', 'eng', None]:
        result = search_books(session, query, limit=5, language=language)
        
        if result and result.get('books'):
            ol_book = result['books'][0]
            return convert_to_book_data(session, ol_book)
    
    # If we have both title and author, try translation
    if title and author:
        translated_title = translate_polish_title(title)
        
        # Try with translated title
        for language in ['pol', 'eng', None]:
            result = search_books(
                session,
                translated_title,
                limit=10,
                language=language
            )
            
            if result and result.get('books'):
                # Find a book that matches the author
                for ol_book in result['books']:
                    book_data = convert_to_book_data(session, ol_book)
                    
                    if author_matches(book_data.author, author):
                        return book_data
        
        # Fallback: search by author only
        result = search_books(session, author, limit=5, language=None)
        if result and result.get('books'):
            ol_book = result['books'][0]
            return convert_to_book_data(session, ol_book)
    
    return None


def search_book(
    session: requests.Session,
    title: Optional[str] = None,
    author: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Main search function with multiple source fallbacks.
    
    Currently only implements Open Library (primary source).
    Returns a dict suitable for embed creation.
    """
    # Primary: Open Library
    result = search_open_library(session, title, author)
    if result:
        return _book_data_to_dict(result)
    
    return None


def _book_data_to_dict(book_data: BookData) -> Dict[str, Any]:
    """Convert BookData dataclass to dictionary for embed creation."""
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
    """
    Validate search parameters.
    
    Returns (is_valid, error_message).
    At least one of title or author must be provided.
    """
    if not title and not author:
        return False, "Please provide at least a title or an author!"
    return True, None
