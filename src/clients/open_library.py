import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from urllib.parse import quote
import requests

from config import OPEN_LIBRARY, RATE_LIMIT

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


_last_request_time: float = 0.0


def _rate_limited_request(
    session: requests.Session,
    url: str,
    params: Optional[Dict] = None,
    timeout: int = 10
) -> requests.Response:
    global _last_request_time
    current_time = time.time()
    time_since_last = current_time - _last_request_time
    if time_since_last < RATE_LIMIT.request_delay:
        delay = RATE_LIMIT.request_delay - time_since_last
        logger.debug(f"Rate limiting: sleeping for {delay:.2f}s")
        time.sleep(delay)
    
    response = session.get(url, params=params, timeout=timeout)
    _last_request_time = time.time()
    return response


def _make_request_with_retry(
    session: requests.Session,
    url: str,
    params: Optional[Dict] = None,
    max_retries: int = RATE_LIMIT.max_retries
) -> Optional[Dict]:
    for attempt in range(max_retries):
        try:
            response = _rate_limited_request(session, url, params)
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
    limit: int = 10,
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
    
    if work_key.startswith('/works/'):
        work_key = work_key[7:]
    
    url = f"{OPEN_LIBRARY.base_url}{OPEN_LIBRARY.works_endpoint}/{work_key}.json"
    return _make_request_with_retry(session, url)


def get_edition_details(
    session: requests.Session,
    edition_key: str
) -> Optional[Dict]:
    logger.info(f"Getting edition details for: {edition_key}")
    
    if edition_key.startswith('/books/'):
        edition_key = edition_key[7:]
    
    url = f"{OPEN_LIBRARY.base_url}{OPEN_LIBRARY.books_endpoint}/{edition_key}.json"
    return _make_request_with_retry(session, url)


def _extract_description(work_details: Optional[Dict]) -> str:
    if not work_details:
        return "No description available."
    
    desc = work_details.get('description')
    if isinstance(desc, dict):
        desc = desc.get('value', '')
    
    if desc and len(str(desc).strip()) > 10:
        return str(desc).strip()
    
    first_sentence = work_details.get('first_sentence')
    if isinstance(first_sentence, dict):
        first_sentence = first_sentence.get('value', '')
    if first_sentence and len(str(first_sentence).strip()) > 5:
        return f"First sentence: {str(first_sentence).strip()}"
    
    return "No description available."


def fetch_description(
    session: requests.Session,
    work_key: Optional[str]
) -> str:
    if not work_key:
        return "No description available."
    
    try:
        details = get_book_details(session, work_key)
        return _extract_description(details)
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch description for {work_key}: {e}")
        return "No description available."


def _get_cover_url(ol_book: Dict, session: requests.Session) -> str:
    cover_id = ol_book.get('cover_i')
    if cover_id:
        return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    
    isbns = ol_book.get('isbn', [])
    if isbns:
        isbn = isbns[0].replace("-", "").replace(" ", "")
        return f"{OPEN_LIBRARY.covers_url}/b/isbn/{isbn}-M.jpg"
    
    return ""


def _build_goodreads_link(title: Optional[str], author: Optional[str]) -> str:
    if title:
        return f"https://www.goodreads.com/search?q={quote(title, safe='')}"
    if author:
        return f"https://www.goodreads.com/search?q={quote(author, safe='')}"
    return "https://www.goodreads.com"


def convert_to_book_data(
    session: requests.Session,
    ol_book: Dict
) -> BookData:
    authors = ol_book.get('author_name', [])
    author = ', '.join(authors) if authors else "Unknown Author"
    
    rating = ol_book.get('ratings_average')
    if rating is not None:
        rating = float(rating)
    
    cover_url = _get_cover_url(ol_book, session)
    description = fetch_description(session, ol_book.get('key'))
    
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
        'User-Agent': 'Discord-Book-Bot/1.0 (https://github.com/your-repo)'
    })
    return session
