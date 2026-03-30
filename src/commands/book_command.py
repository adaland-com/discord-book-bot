import logging
from typing import Optional
import discord
from discord import app_commands

from src.clients.open_library import (
    search_books,
    fetch_and_convert_book_data,
    build_search_query,
    APIError,
)
from src.embed_service import (
    create_book_embed,
    create_no_results_message,
    create_error_embed,
)
from config import SEARCH_MAX_RESULTS

logger = logging.getLogger(__name__)


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
    ) -> None:
        # Validate search params first (before deferring)
        if not title and not author:
            embed = create_error_embed("Please provide at least a title or an author!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer()
        
        query = build_search_query(title, author)
        
        location = "DM" if interaction.guild is None else f"guild={interaction.guild.name}"
        logger.info(f"[/book] user={interaction.user.name} query='{query}' {location}")
        
        session = interaction.client.session
        try:
            await interaction.client.rate_limiter.acquire()
            result = await search_books(session, query, limit=SEARCH_MAX_RESULTS)
            
            if result and result.get('books'):
                await interaction.client.rate_limiter.acquire()
                book_info = await fetch_and_convert_book_data(session, result['books'][0])
            else:
                book_info = None
        except APIError as e:
            logger.error(f"[/book] API error: {e}")
            embed = create_error_embed("Open Library API is unavailable. Please try again later.")
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        except Exception as e:
            logger.error(f"[/book] Unexpected error: {type(e).__name__}: {e}")
            embed = create_error_embed("Search failed due to an unexpected error.")
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        if book_info is None:
            message = create_no_results_message(title, author)
            await interaction.followup.send(message)
            return
        
        embed = create_book_embed(book_info)
        await interaction.followup.send(embed=embed)
    
    return book_command
