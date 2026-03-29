"""Services package."""
from src.services.book_service import (
    search_book,
    search_open_library,
    validate_search_params,
)
from src.services.embed_service import (
    create_book_embed,
    create_help_embed,
    create_no_results_message,
    create_error_embed,
)
from src.services.logging_service import (
    log_usage,
    log_search_attempt,
    format_log_message,
)

__all__ = [
    # Book service
    'search_book',
    'search_open_library',
    'validate_search_params',
    # Embed service
    'create_book_embed',
    'create_help_embed',
    'create_no_results_message',
    'create_error_embed',
    # Logging service
    'log_usage',
    'log_search_attempt',
    'format_log_message',
]
