import asyncio
import logging
from typing import Optional
import discord
from discord import app_commands
import requests

from src.clients.open_library import (
    search_books,
    fetch_and_convert_book_data,
    build_search_query,
)
from src.embed_service import (
    create_book_embed,
    create_no_results_message,
    create_error_embed,
)
from config import EMBED, SEARCH

logger = logging.getLogger(__name__)


async def _handle_book_command(
    interaction: discord.Interaction,
    title: Optional[str] = None,
    author: Optional[str] = None
) -> None:
    await interaction.response.defer()
    
    # Validate search params
    if not title and not author:
        embed = create_error_embed("Please provide at least a title or an author!")
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    query_parts = []
    if title:
        query_parts.append(f"title={title}")
    if author:
        query_parts.append(f"author={author}")
    query_str = "&".join(query_parts)
    
    location = "DM" if interaction.guild is None else f"guild={interaction.guild.name}"
    logger.info(f"[/book] user={interaction.user.name} query='{query_str}' {location}")
    
    session = interaction.client.session
    try:
        query = build_search_query(title, author)
        
        # Rate limit before API call
        await interaction.client.rate_limiter.acquire()
        result = await asyncio.to_thread(search_books, session, query, limit=SEARCH.max_results)
        
        if result and result.get('books'):
            # Rate limit before API call
            await interaction.client.rate_limiter.acquire()
            book_info = await asyncio.to_thread(fetch_and_convert_book_data, session, result['books'][0])
        else:
            book_info = None
    except requests.RequestException as e:
        logger.error(f"[/book] search_failed error={type(e).__name__}: {e}")
        embed = create_error_embed("Search failed. Please try again.")
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    if book_info is None:
        message = create_no_results_message(title, author)
        await interaction.followup.send(message)
        return
    
    embed = create_book_embed(book_info)
    
    embed.add_field(
        name=f"{EMBED.emoji_archive} Anna's Archive",
        value=EMBED.archive_link,
        inline=False
    )
    
    await interaction.followup.send(embed=embed)


def create_book_command() -> app_commands.Command:
    @app_commands.command(
        name="book",
        description="Search for a book anywhere (DM, servers, group chats)"
    )
    @app_commands.describe(
        title="Book title (required if no author provided)",
        author="Book author (required if no title provided)"
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=True,
        private_channels=True
    )
    @app_commands.allowed_installs(
        guilds=True,
        users=True
    )
    async def book_command(
        interaction: discord.Interaction,
        title: Optional[str] = None,
        author: Optional[str] = None
    ):
        await _handle_book_command(interaction, title, author)
    
    return book_command
