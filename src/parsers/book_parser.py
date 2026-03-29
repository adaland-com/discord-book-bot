from typing import Optional


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
