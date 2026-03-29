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
