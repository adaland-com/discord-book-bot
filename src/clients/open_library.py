import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from urllib.parse import quote
import requests

from config import OPEN_LIBRARY, RATE_LIMIT, SEARCH

# Module-level constants
_MIN_DESC_LENGTH = 10
_MIN_SENTENCE_LENGTH = 5
_COVER_SIZE_SUFFIX = SEARCH.cover_size

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BookData:
    title: str
    author: str
    rating: Optional[float]
    description: str
    cover_url: str
    publication_year: Optional[int]
    url: str
    source: str
    goodreads_url: str
    language: List[str]
    edition_count: int


def _make_request_with_retry(
    session: requests.Session,
    url: str,
    params: Optional[Dict] = None,
    max_retries: int = RATE_LIMIT.max_retries,
    timeout: int = SEARCH.timeout
) -> Optional[Dict]:
    """Make HTTP request with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            response = session.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                logger.error(f"Request failed after {max_retries} attempts: {e}")
                return None
            
            wait_time = RATE_LIMIT.retry_delay * (2 ** attempt)
            logger.warning(f"Request failed (attempt {attempt + 1}), retrying in {wait_time}s: {e}")
            time.sleep(wait_time)
    
    return None


def search_books(
    session: requests.Session,
    query: str,
    limit: int = SEARCH.max_results,
    language: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    logger.info(f"Searching Open Library for: '{query}' (limit={limit})")
    
    url = f"{OPEN_LIBRARY.base_url}{OPEN_LIBRARY.search_endpoint}"
    params = {
        'q': query,
        'limit': limit,
        'fields': 'key,title,description,author_name,author_key,first_publish_year,cover_i,ratings_average,subject,language,edition_count,isbn'
    }
    
    if language:
        params['language'] = language
    
    data = _make_request_with_retry(session, url, params)
    if data is None:
        return None
    
    result = {
        'numFound': data.get('numFound', 0),
        'books': data.get('docs', [])
    }
    
    return result


def get_book_details(
    session: requests.Session,
    work_key: str
) -> Optional[Dict]:
    logger.info(f"Getting book details for work: {work_key}")
    
    # Remove '/works/' prefix (7 characters) from work key
    if work_key.startswith('/works/'):
        work_key = work_key[len('/works/'):]
    
    url = f"{OPEN_LIBRARY.base_url}{OPEN_LIBRARY.works_endpoint}/{work_key}.json"
    return _make_request_with_retry(session, url)


def get_edition_details(
    session: requests.Session,
    edition_key: str
) -> Optional[Dict]:
    logger.info(f"Getting edition details for: {edition_key}")
    
    # Remove '/books/' prefix (7 characters) from edition key
    if edition_key.startswith('/books/'):
        edition_key = edition_key[len('/books/'):]
    
    url = f"{OPEN_LIBRARY.base_url}{OPEN_LIBRARY.books_endpoint}/{edition_key}.json"
    return _make_request_with_retry(session, url)


def _extract_description(data: Dict) -> str:
    """Extract description from work details or search result data.
    
    Handles both full work details and search result data since they share
    the same field structure for description and first_sentence.
    """
    desc = data.get('description')
    if isinstance(desc, dict):
        desc = desc.get('value', '')
    
    if desc and len(str(desc).strip()) > _MIN_DESC_LENGTH:
        return str(desc).strip()
    
    first_sentence = data.get('first_sentence')
    if isinstance(first_sentence, dict):
        first_sentence = first_sentence.get('value', '')
    if first_sentence and len(str(first_sentence).strip()) > _MIN_SENTENCE_LENGTH:
        return f"First sentence: {str(first_sentence).strip()}"
    
    return "No description available."


def _extract_description_from_search(ol_book: Dict) -> str:
    """Extract description from search result data without HTTP call."""
    return _extract_description(ol_book)


def fetch_description(
    session: requests.Session,
    work_key: Optional[str]
) -> Optional[str]:
    """Fetch book description. Returns None on error, empty string if no description."""
    if not work_key:
        return None
    
    try:
        details = get_book_details(session, work_key)
        if details is None:
            return None
        desc = _extract_description(details)
        # Return empty string for "no description" cases, None for errors
        return "" if desc == "No description available." else desc
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch description for {work_key}: {e}")
        return None


def _get_cover_url(ol_book: Dict) -> str:
    cover_id = ol_book.get('cover_i')
    if cover_id:
        return f"https://covers.openlibrary.org/b/id/{cover_id}{_COVER_SIZE_SUFFIX}"
    
    isbns = ol_book.get('isbn', [])
    if isbns and isinstance(isbns[0], str):
        # Use translate for single-pass character removal
        isbn = isbns[0].translate(str.maketrans('', '', '- '))
        return f"{OPEN_LIBRARY.covers_url}/b/isbn/{isbn}{_COVER_SIZE_SUFFIX}"
    
    return ""


def _build_goodreads_link(title: Optional[str], author: Optional[str]) -> str:
    if title and author:
        return f"https://www.goodreads.com/search?q={quote(f'title:{title} author:{author}', safe='')}"  
    if title:
        return f"https://www.goodreads.com/search?q={quote(f'title:{title}', safe='')}"
    if author:
        return f"https://www.goodreads.com/search?q={quote(f'author:{author}', safe='')}"
    return "https://www.goodreads.com"


def fetch_and_convert_book_data(
    session: requests.Session,
    ol_book: Dict
) -> BookData:
    """Convert Open Library search result to BookData.
    
    Uses description from search results if available, otherwise fetches details.
    """
    authors = ol_book.get('author_name', [])
    author = ', '.join(authors) if authors else "Unknown Author"
    
    rating = ol_book.get('ratings_average')
    if rating is not None:
        rating = float(rating)
    
    cover_url = _get_cover_url(ol_book)
    
    # Use description from search results if available, skip HTTP call
    raw_description = _extract_description_from_search(ol_book)
    if raw_description and raw_description != "No description available.":
        description = raw_description
    else:
        # Fall back to fetching details via HTTP
        fetched = fetch_description(session, ol_book.get('key'))
        description = fetched if fetched is not None else "No description available."
    
    title = ol_book.get('title', 'Unknown Title')
    
    return BookData(
        title=title,
        author=author,
        rating=rating,
        description=description,
        cover_url=cover_url,
        publication_year=ol_book.get('first_publish_year'),
        url='https://openlibrary.org' + ol_book.get('key', ''),
        source='Open Library',
        goodreads_url=_build_goodreads_link(title, author),
        language=ol_book.get('language', []),
        edition_count=ol_book.get('edition_count', 0)
    )


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Discord-Book-Bot/1.0 (https://github.com/adaland-com/discord-book-bot)'
    })
    return session


def build_search_query(title: Optional[str], author: Optional[str]) -> str:
    parts = []
    if title:
        # Escape quotes to prevent query injection
        safe_title = title.replace('"', '\\"')
        parts.append(f'title:"{safe_title}"')
    if author:
        # Escape quotes to prevent query injection
        safe_author = author.replace('"', '\\"')
        parts.append(f'author:"{safe_author}"')
    return ' '.join(parts)
