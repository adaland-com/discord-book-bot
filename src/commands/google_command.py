"""Google command handler (utility command from bot2.py)."""
import discord
from discord import app_commands

from src.services.logging_service import log_usage


def create_google_command() -> app_commands.Command:
    """Create the /google slash command."""
    
    @app_commands.command(
        name="google",
        description="Sends a link to Google"
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
    async def google_command(interaction: discord.Interaction):
        log_usage(
            interaction.user.name,
            "/google",
            "Slash",
            "DM" if interaction.guild is None else f"Server: {interaction.guild.name}"
        )
        
        view = discord.ui.View()
        button = discord.ui.Button(
            label="Open Google",
            url="https://www.google.com"
        )
        view.add_item(button)
        
        await interaction.response.send_message(
            "Here is your handy link:",
            view=view
        )
    
    return google_command
