"""Centralized configuration for the Discord Book Bot."""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class DiscordConfig:
    """Discord bot configuration (immutable)."""
    token: str
    tmp_token: str
    prefix: str = "!"
    restrict_dm_to_guild_members: bool = False


@dataclass(frozen=True)
class OpenLibraryConfig:
    """Open Library API configuration (immutable)."""
    base_url: str = "https://openlibrary.org"
    search_endpoint: str = "/search.json"
    works_endpoint: str = "/works"
    books_endpoint: str = "/books"
    covers_url: str = "https://covers.openlibrary.org"


@dataclass(frozen=True)
class GoogleBooksConfig:
    """Google Books API configuration (immutable)."""
    api_key: str | None
    base_url: str = "https://www.googleapis.com/books/v1"


@dataclass(frozen=True)
class RateLimitConfig:
    """Rate limiting configuration (immutable)."""
    request_delay: float = 1.0
    max_retries: int = 3
    retry_delay: float = 2.0


@dataclass(frozen=True)
class CacheConfig:
    """Cache configuration (immutable)."""
    ttl_seconds: int = 3600
    enabled: bool = True


@dataclass(frozen=True)
class EmbedConfig:
    """Discord embed configuration (immutable)."""
    color: int = 0x00b4d8
    max_description_length: int = 200


@dataclass(frozen=True)
class SearchConfig:
    """Search configuration (immutable)."""
    max_results: int = 5
    timeout: int = 10


# Global configuration instances
DISCORD = DiscordConfig(
    token=os.getenv('TMP_DISCORD_TOKEN', ''),
    tmp_token=os.getenv('TMP_DISCORD_TOKEN', ''),
    prefix=os.getenv('BOT_PREFIX', '!'),
    restrict_dm_to_guild_members=os.getenv(
        'RESTRICT_DM_TO_GUILD_MEMBERS', 'false'
    ).lower() == 'true'
)

OPEN_LIBRARY = OpenLibraryConfig()

GOOGLE_BOOKS = GoogleBooksConfig(
    api_key=os.getenv('GOOGLE_BOOKS_API_KEY')
)

RATE_LIMIT = RateLimitConfig()

CACHE = CacheConfig(
    ttl_seconds=int(os.getenv('CACHE_TTL', '3600')),
    enabled=os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
)

EMBED = EmbedConfig()

SEARCH = SearchConfig()
