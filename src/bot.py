import logging
import discord
from discord.ext import commands
from discord import app_commands

from config import DISCORD
from src.commands import (
    create_book_command,
    create_help_command,
)
from src.clients.open_library import create_session

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BookBot(commands.Bot):
    
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(
            command_prefix="",
            intents=intents,
            help_command=None
        )
        
        self.session = create_session()
    
    async def setup_hook(self):
        self.tree.add_command(create_book_command())
        self.tree.add_command(create_help_command())
        
        print("Syncing slash commands...")
        await self.tree.sync()
        print("Slash commands synced!")
    
    async def on_ready(self):
        print(f"Logged in as {self.user}!")
        print(f"Bot ready for DMs and servers with slash commands.")


def main():
    token = DISCORD.token
    
    if not token:
        print("Error: No Discord token found. Please set DISCORD_TOKEN in .env")
        return
    
    bot = BookBot()
    bot.run(token)


if __name__ == "__main__":
    main()
