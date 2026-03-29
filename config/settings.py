"""Centralized configuration for the Discord Book Bot."""
import os
from dotenv import load_dotenv

load_dotenv()


def _parse_bool(value: str) -> bool:
    """Parse a string value as boolean (case-insensitive)."""
    return value.lower() in ('true', '1', 'yes', 'on')


# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', '')
DISCORD_RESTRICT_DM = _parse_bool(os.getenv('RESTRICT_DM_TO_GUILD_MEMBERS', 'false'))

# Open Library API
OPEN_LIBRARY_BASE_URL = "https://openlibrary.org"
OPEN_LIBRARY_SEARCH_ENDPOINT = "/search.json"
OPEN_LIBRARY_WORKS_ENDPOINT = "/works"
OPEN_LIBRARY_BOOKS_ENDPOINT = "/books"
OPEN_LIBRARY_COVERS_URL = "https://covers.openlibrary.org"

# Rate Limiting
RATE_LIMIT_REQUEST_DELAY = 1.0
RATE_LIMIT_MAX_RETRIES = 3
RATE_LIMIT_RETRY_DELAY = 2.0

# Embed Settings
EMBED_COLOR = 0x00b4d8
EMBED_ERROR_COLOR = 0xFF0000
EMBED_MAX_DESCRIPTION_LENGTH = 200
EMBED_ARCHIVE_LINK = "https://shadowlibraries.github.io/DirectDownloads/AnnasArchive/"
EMBED_EMOJI_AUTHOR = "👤"
EMBED_EMOJI_RATING = "⭐"
EMBED_EMOJI_YEAR = "�"
EMBED_EMOJI_LINK = "🔗"
EMBED_EMOJI_ARCHIVE = "🏴‍☠️"

# Search Settings
SEARCH_MAX_RESULTS = 5
SEARCH_TIMEOUT = 10
SEARCH_COVER_SIZE = "-M.jpg"


# Legacy compatibility - config objects that mimic old dataclass structure
class _ConfigNamespace:
    """Simple namespace for legacy compatibility."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k.lower(), v)


# Backwards compatibility exports
DISCORD = _ConfigNamespace(
    token=DISCORD_TOKEN,
    restrict_dm_to_guild_members=DISCORD_RESTRICT_DM
)

OPEN_LIBRARY = _ConfigNamespace(
    base_url=OPEN_LIBRARY_BASE_URL,
    search_endpoint=OPEN_LIBRARY_SEARCH_ENDPOINT,
    works_endpoint=OPEN_LIBRARY_WORKS_ENDPOINT,
    books_endpoint=OPEN_LIBRARY_BOOKS_ENDPOINT,
    covers_url=OPEN_LIBRARY_COVERS_URL
)

RATE_LIMIT = _ConfigNamespace(
    request_delay=RATE_LIMIT_REQUEST_DELAY,
    max_retries=RATE_LIMIT_MAX_RETRIES,
    retry_delay=RATE_LIMIT_RETRY_DELAY
)

EMBED = _ConfigNamespace(
    color=EMBED_COLOR,
    error_color=EMBED_ERROR_COLOR,
    max_description_length=EMBED_MAX_DESCRIPTION_LENGTH,
    archive_link=EMBED_ARCHIVE_LINK,
    emoji_author=EMBED_EMOJI_AUTHOR,
    emoji_rating=EMBED_EMOJI_RATING,
    emoji_year=EMBED_EMOJI_YEAR,
    emoji_link=EMBED_EMOJI_LINK,
    emoji_archive=EMBED_EMOJI_ARCHIVE
)

SEARCH = _ConfigNamespace(
    max_results=SEARCH_MAX_RESULTS,
    timeout=SEARCH_TIMEOUT,
    cover_size=SEARCH_COVER_SIZE
)
