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
   TMP_DISCORD_TOKEN=your_discord_bot_token_here
   ```

3. (Optional) Add Google Books API key for fallback searches:
   ```
   GOOGLE_BOOKS_API_KEY=your_google_books_api_key_here
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

## Project Structure

```
discord-book-bot/
├── bot.py                 # Main bot file with Discord commands
├── book_searcher.py       # Multi-source book search logic
├── open_library_client.py # Open Library API client
├── config.py             # Bot configuration
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── .env.example          # Example environment file
├── README.md            # This file
├── run_bot.bat          # Windows batch file to run the bot
├── run_tests.py         # Test runner
├── tests/               # Test suite
└── docs/                # Documentation and implementation notes
```

## Dependencies

- `discord.py` - Discord API wrapper
- `requests` - HTTP requests for API calls
- `beautifulsoup4` - Web scraping (legacy fallback)
- `googlesearch-python` - Google search functionality (legacy fallback)
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

3. **Polish book search issues**
   - Open Library has excellent Polish literature coverage
   - Try both Polish and English titles
   - Polish characters are handled automatically

## Testing

```bash
# Run all tests
python run_tests.py

# Or use pytest
pytest

# Run with verbose output
pytest -v
```

## License

This project is open source and available under the MIT License.

## Additional Documentation

For implementation details, technical notes, and case studies, see the `docs/` folder:
- `docs/implementation-notes.md` - Technical implementation details
- `docs/polish-setup-guide.md` - Polish language setup guide
- `docs/case-studies.md` - Bug fixes and solutions
