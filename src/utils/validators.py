from typing import Optional


def validate_non_empty(value: Optional[str]) -> bool:
    return value is not None and len(value.strip()) > 0


def sanitize_input(value: str, max_length: int = 200) -> str:
    if not value:
        return ""
    sanitized = value.strip()
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    return sanitized
