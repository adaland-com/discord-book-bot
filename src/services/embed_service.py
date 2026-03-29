"""Pure functions for building Discord embeds."""
from typing import Dict, Any, Optional
import discord
from config import EMBED


def create_book_embed(book_info: Dict[str, Any]) -> discord.Embed:
    """Create a Discord embed from book information."""
    embed = discord.Embed(
        title=book_info.get('title', 'Unknown Title'),
        url=book_info.get('url'),
        color=EMBED.color
    )
    
    if book_info.get('author'):
        embed.add_field(
            name="👤 Author",
            value=book_info['author'],
            inline=False
        )
    
    if book_info.get('rating'):
        embed.add_field(
            name="⭐ Rating",
            value=f"{book_info['rating']}/5.0",
            inline=True
        )
    
    if book_info.get('publication_year'):
        embed.add_field(
            name="📅 Year",
            value=str(book_info['publication_year']),
            inline=True
        )
    
    desc = book_info.get('description', "No description available.")
    if len(desc) > EMBED.max_description_length:
        desc = desc[:EMBED.max_description_length] + "..."
    embed.description = desc
    
    if book_info.get('cover_url'):
        embed.set_thumbnail(url=book_info['cover_url'])
    
    source = book_info.get('source', 'Unknown')
    embed.set_footer(text=f"Source: {source}")
    
    # Add external links
    if book_info.get('goodreads_url'):
        embed.add_field(
            name="🔗 Goodreads",
            value=book_info['goodreads_url'],
            inline=False
        )
    
    return embed


def create_help_embed() -> discord.Embed:
    """Create the help menu embed."""
    embed = discord.Embed(
        title="Book Search Help",
        color=EMBED.color
    )
    embed.description = (
        "Use `/book` to search for books anywhere on Discord!\n\n"
        "**Commands:**\n"
        "• `/book <title>` - search by title\n"
        "• `/book title: <title> author: <author>` - exact search\n\n"
        "**Direct Messages:** Send a message without prefix to search.\n\n"
        "Add the app to your account to use it in DMs with friends."
    )
    return embed


def create_no_results_message(
    title: Optional[str] = None,
    author: Optional[str] = None
) -> str:
    """Create a 'no results found' message."""
    parts = []
    if title:
        parts.append(f"title '{title}'")
    if author:
        if title:
            parts.append(f"by author '{author}'")
        else:
            parts.append(f"author '{author}'")
    
    search_desc = " ".join(parts) if parts else "your query"
    return f"No book found for {search_desc}."


def create_error_embed(message: str) -> discord.Embed:
    """Create an error embed."""
    embed = discord.Embed(
        title="Error",
        description=message,
        color=0xFF0000  # Red
    )
    return embed
