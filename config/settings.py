"""Centralized configuration for the Discord Book Bot."""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _parse_bool(value: str) -> bool:
    """Parse a string value as boolean."""
    return value.lower() in ('true', '1', 'yes', 'on')


@dataclass(frozen=True)
class DiscordConfig:
    token: str
    restrict_dm_to_guild_members: bool = False

@dataclass(frozen=True)
class OpenLibraryConfig:
    base_url: str = "https://openlibrary.org"
    search_endpoint: str = "/search.json"
    works_endpoint: str = "/works"
    books_endpoint: str = "/books"
    covers_url: str = "https://covers.openlibrary.org"

@dataclass(frozen=True)
class RateLimitConfig:
    request_delay: float = 1.0
    max_retries: int = 3
    retry_delay: float = 2.0


@dataclass(frozen=True)
class EmbedConfig:
    color: int = 0x00b4d8
    error_color: int = 0xFF0000
    max_description_length: int = 200
    archive_link: str = "https://shadowlibraries.github.io/DirectDownloads/AnnasArchive/"
    emoji_author: str = "👤"
    emoji_rating: str = "⭐"
    emoji_year: str = "📅"
    emoji_link: str = "🔗"
    emoji_archive: str = "🏴‍☠️"

@dataclass(frozen=True)
class SearchConfig:
    max_results: int = 5
    timeout: int = 10
    cover_size: str = "-M.jpg"

# Global configuration instances
DISCORD = DiscordConfig(
    token=os.getenv('DISCORD_TOKEN', ''),
    restrict_dm_to_guild_members=_parse_bool(
        os.getenv('RESTRICT_DM_TO_GUILD_MEMBERS', 'false')
    )
)

OPEN_LIBRARY = OpenLibraryConfig()

RATE_LIMIT = RateLimitConfig()

EMBED = EmbedConfig()

SEARCH = SearchConfig()
