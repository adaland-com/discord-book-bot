# Discord Book Search Bot

A Discord bot that searches for books using Open Library API and returns detailed book information including author, rating, and description.

## Features

- 🔍 Search for books using `/book title: <book title> author: <author name>`
- 📚 Returns book information from Open Library API
- 🌐 **Excellent Polish literature coverage** - Pan Tadeusz, Lalka, Quo Vadis, and more
- 👤 Shows author information
- ⭐ Displays book ratings
- 📖 Includes book descriptions and cover images
- 🔗 Direct links to Open Library pages
- 🚀 **No rate limiting** - Uses reliable API instead of web scraping
- 💾 **Built-in caching** for faster responses on repeated searches
- 👨‍💼 **Author search** - Search by author name with or without title
- 📱 **DM support** - Works in private messages without prefix

## Setup

### Prerequisites

- Python 3.8 or higher
- Discord account
- Discord Bot Token

### Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token
5. Enable **Message Content Intent**

### Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your Discord bot token:
   ```
   DISCORD_TOKEN =your_discord_bot_token_here
   ```

### Running the Bot

```bash
python bot.py
```

## Usage

### Server Commands (with prefix)

- `/book title: Book Title` - Search for a specific book
- `/book author: Author Name` - Search for books by a specific author
- `/book title: Book Title author: Author Name` - Search with both title and author
- `/book Book Title` - Simple search (treated as title)

### DM Commands (no prefix)

- `Book Title` - Simple search
- `title: Book Title` - Search with title parameter
- `author: Author Name` - Search by author
- `title: Book Title author: Author Name` - Combined search

### Examples

```
/book title: Pan Tadeusz
/book author: Adam Mickiewicz
/book title: Harry Potter author: J.K. Rowling
/book 1984
```

The bot will respond with a rich embed containing:
- Book title with Open Library link
- Author information
- Rating (if available)
- Publication year (if available)
- Book description
- Cover image (if available)
- Source information (Open Library, Google Books, etc.)

## Bot Permissions

The bot requires the following permissions in your Discord server:
- Read Messages/View Channels
- Send Messages
- Embed Links

## Dependencies

- `discord.py` - Discord API wrapper
- `requests` - HTTP requests for API calls
- `beautifulsoup4` - Web scraping (legacy fallback)
- `python-dotenv` - Environment variable management

## Troubleshooting

### Common Issues

1. **Bot doesn't respond to commands**
   - Check that the bot has the correct permissions
   - Verify the Discord token is correct
   - Make sure Message Content Intent is enabled

2. **Book not found**
   - Try using the exact book title
   - Check if the book exists on Open Library
   - Some books might not be available in Open Library's database

## License

This project is open source and available under the MIT License.
