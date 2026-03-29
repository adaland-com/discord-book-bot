import discord
from discord import app_commands

from src.services.embed_service import create_help_embed
from src.services.logging_service import log_usage


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
        log_usage(
            interaction.user.name,
            "/help",
            None,
            "DM" if interaction.guild is None else f"Server: {interaction.guild.name}"
        )
        
        embed = create_help_embed()
        await interaction.response.send_message(embed=embed)
    
    return help_command
