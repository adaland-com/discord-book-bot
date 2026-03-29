import logging
import discord
from discord import app_commands

from src.services.embed_service import create_help_embed

logger = logging.getLogger(__name__)


def create_help_command() -> app_commands.Command:
    
    @app_commands.command(
        name="help",
        description="Show help menu and instructions"
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
    async def help_command(interaction: discord.Interaction):
        location = "DM" if interaction.guild is None else f"Server: {interaction.guild.name}"
        logger.info(f"{interaction.user.name} used /help | Location: {location}")
        
        embed = create_help_embed()
        await interaction.response.send_message(embed=embed)
    
    return help_command
