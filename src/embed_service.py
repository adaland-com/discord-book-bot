from typing import Optional
import discord
from config import EMBED_COLOR, EMBED_ERROR_COLOR, EMBED_MAX_DESCRIPTION_LENGTH, EMBED_EMOJI_AUTHOR, EMBED_EMOJI_RATING, EMBED_EMOJI_YEAR, EMBED_EMOJI_LINK, EMBED_EMOJI_ARCHIVE
from src.clients.open_library import BookData


def create_book_embed(book_info: BookData) -> discord.Embed:
    embed = discord.Embed(
        title=book_info.title,
        url=book_info.url,
        color=EMBED_COLOR
    )
    
    if book_info.author:
        embed.add_field(
            name=f"{EMBED_EMOJI_AUTHOR} Author",
            value=book_info.author,
            inline=False
        )
    
    if book_info.rating:
        embed.add_field(
            name=f"{EMBED_EMOJI_RATING} Rating",
            value=f"{book_info.rating}/5.0",
            inline=True
        )
    
    if book_info.publication_year:
        embed.add_field(
            name=f"{EMBED_EMOJI_YEAR} Year",
            value=str(book_info.publication_year),
            inline=True
        )
    
    desc = book_info.description if book_info.description else "No description available."
    if len(desc) > EMBED_MAX_DESCRIPTION_LENGTH:
        desc = desc[:EMBED_MAX_DESCRIPTION_LENGTH] + "..."
    embed.description = desc
    
    if book_info.cover_url:
        embed.set_thumbnail(url=book_info.cover_url)
    
    embed.set_footer(text=f"Source: {book_info.source}")
    
    embed.add_field(
        name=f"{EMBED_EMOJI_LINK} Goodreads",
        value=book_info.goodreads_url,
        inline=False
    )
    
    return embed


def create_help_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Book Search Help",
        color=EMBED_COLOR
    )
    embed.description = (
        "Use `/book` to search for books anywhere on Discord!\n\n"
        "**How to search:**\n"
        "1. Type `/book`\n"
        "2. Fill in the \"title\" field for title search\n"
        "3. Fill in the \"author\" field for author search\n"
        "4. Fill both for exact matching\n\n"
        "**Works in:** Servers, DMs, and Group DMs\n\n"
        "Add the app to your account to use it anywhere."
    )
    return embed


def create_no_results_message(
    title: Optional[str] = None,
    author: Optional[str] = None
) -> str:
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
    embed = discord.Embed(
        title="Error",
        description=message,
        color=EMBED_ERROR_COLOR
    )
    return embed
