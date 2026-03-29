"""Unified Discord Book Bot - merges bot.py and bot2.py functionality."""
import discord
from discord.ext import commands
from discord import app_commands

from config import DISCORD
from src.commands import (
    create_book_command,
    create_help_command,
    create_google_command,
)
from src.clients.open_library import create_session


class BookBot(commands.Bot):
    
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(
            command_prefix=DISCORD.prefix,
            intents=intents,
            help_command=None
        )
        
        self.session = create_session()
    
    async def setup_hook(self):
        self.tree.add_command(create_book_command())
        self.tree.add_command(create_help_command())
        self.tree.add_command(create_google_command())
        
        print("Syncing slash commands...")
        await self.tree.sync()
        print("Slash commands synced!")
    
    async def on_ready(self):
        """Called when bot is ready."""
        print(f"Logged in as {self.user}!")
        print(f"Bot ready for DMs and servers with slash commands.")
    
    async def on_message(self, message: discord.Message):
        """Handle messages - only process commands (no privileged intent needed)."""
        if message.author == self.user:
            return
        await self.process_commands(message)


def main():
    """Entry point for the bot."""
    token = DISCORD.token
    
    if not token:
        print("Error: No Discord token found. Please set DISCORD_TOKEN  in .env")
        return
    
    bot = BookBot()
    bot.run(token)


if __name__ == "__main__":
    main()
