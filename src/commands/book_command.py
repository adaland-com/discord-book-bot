import asyncio
import logging
from typing import Optional
import discord
from discord import app_commands

from src.services.book_service import search_open_library, validate_search_params
from src.services.embed_service import (
    create_book_embed,
    create_no_results_message,
    create_error_embed,
)
from src.services.logging_service import log_usage
from config import EMBED

logger = logging.getLogger(__name__)



class BookCommandHandler:
    
    async def handle(
        self,
        interaction: discord.Interaction,
        title: Optional[str] = None,
        author: Optional[str] = None
    ) -> None:
        await interaction.response.defer()
        
        is_valid, error = validate_search_params(title, author)
        if not is_valid:
            embed = create_error_embed(error)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        query_parts = []
        if title:
            query_parts.append(f"title: {title}")
        if author:
            query_parts.append(f"author: {author}")
        query_str = " | ".join(query_parts)
        
        log_usage(
            interaction.user.name,
            "/book",
            query_str,
            "DM" if interaction.guild is None else f"Server: {interaction.guild.name}"
        )
        
        session = interaction.client.session
        try:
            book_info = await asyncio.to_thread(search_open_library, session, title, author)
        except Exception as e:
            logger.error(f"Search failed: {e}")
            embed = create_error_embed("Search failed. Please try again.")
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        if book_info is None:
            message = create_no_results_message(title, author)
            await interaction.followup.send(message)
            return
        
        embed = create_book_embed(book_info)
        
        embed.add_field(
            name="🏴‍☠️ Anna's Archive",
            value=EMBED.archive_link,
            inline=False
        )
        
        await interaction.followup.send(embed=embed)


def create_book_command() -> app_commands.Command:
    handler = BookCommandHandler()
    
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
        await handler.handle(interaction, title, author)
    
    return book_command
