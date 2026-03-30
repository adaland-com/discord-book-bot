import asyncio
import logging
import time
import discord
from discord import app_commands

from discord.ext import commands

from config import DISCORD, RATE_LIMIT
from src.commands import (
    create_book_command,
    create_help_command,
)
from src.clients.open_library import create_session

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class RateLimiter:
    """Async-compatible rate limiter for Open Library API calls."""
    
    def __init__(self, request_delay: float):
        self._lock = asyncio.Lock()
        self._last_request_time: float = 0.0
        self._request_delay = request_delay
    
    async def acquire(self) -> None:
        """Acquire rate limit, sleeping if necessary."""
        async with self._lock:
            current_time = time.monotonic()
            time_since_last = current_time - self._last_request_time
            delay = max(0, self._request_delay - time_since_last)
            
            if delay > 0:
                await asyncio.sleep(delay)
            
            self._last_request_time = time.monotonic()


class BookBot(commands.Bot):
    
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents, command_prefix="!")
        
        self.session = None
        self.rate_limiter = RateLimiter(RATE_LIMIT.request_delay)
    
    async def setup_hook(self):
        self.session = create_session()
        
        self.tree.add_command(create_book_command())
        self.tree.add_command(create_help_command())
        
        logger.info("Syncing slash commands...")
        await self.tree.sync()
        logger.info("Slash commands synced!")
    
    async def on_ready(self):
        logger.info(f"Logged in as {self.user}!")
        logger.info("Bot ready for DMs and servers with slash commands.")
    
    async def close(self):
        """Clean up resources on shutdown."""
        logger.info("Closing bot session...")
        if self.session:
            await self.session.close()
        await super().close()


def main():
    token = DISCORD.token
    
    if not token:
        logger.error("No Discord token found. Please set DISCORD_TOKEN in .env")
        return
    
    bot = BookBot()
    bot.run(token)


if __name__ == "__main__":
    main()
