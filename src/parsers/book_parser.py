import re
from typing import Tuple, Optional


def parse_query(query: str) -> Tuple[Optional[str], Optional[str]]:
    if not query:
        return None, None
    
    query = query.strip()
    
    title_match = re.search(r'title:\s*([^:]+?)(?:\s+author:|$)', query, re.IGNORECASE)
    author_match = re.search(r'author:\s*(.+?)(?:\s+title:|$)', query, re.IGNORECASE)
    
    if title_match or author_match:
        title = title_match.group(1).strip() if title_match else None
        author = author_match.group(1).strip() if author_match else None
        return title, author
    
    by_match = re.search(r'(.+)\s+by\s+(.+)', query, re.IGNORECASE)
    if by_match:
        return by_match.group(1).strip(), by_match.group(2).strip()
    
    return query, None


def build_search_query(
    title: Optional[str],
    author: Optional[str]
) -> str:
    parts = []
    if title:
        parts.append(f'title:"{title}"')
    if author:
        parts.append(f'author:"{author}"')
    return ' '.join(parts)


def translate_polish_title(title: str) -> str:
    translations = {
        'zachowuj się': 'behave',
        'zachowaj sie': 'behave',
        'pan tadeusz': 'master thaddeus',
        'lalka': 'the doll',
        'quo vadis': 'quo vadis',
        'potop': 'the deluge',
        'ogniem i mieczem': 'with fire and sword',
        'pan wołodyjowski': 'pan michael',
    }
    return translations.get(title.lower(), title)


def author_matches(
    book_author: str,
    search_author: str
) -> bool:
    if not search_author or not book_author:
        return False
    
    book_author_lower = book_author.lower()
    search_author_lower = search_author.lower()
    
    if search_author_lower in book_author_lower:
        return True
    
    search_parts = search_author_lower.split()
    author_names = book_author_lower.split()
    
    return any(
        any(part in name for name in author_names)
        for part in search_parts
    )


def format_book_description(
    description: str,
    max_length: int = 200
) -> str:
    if len(description) <= max_length:
        return description
    return description[:max_length] + "..."
