# Python Virtual Environment Setup

This project now includes a Python virtual environment to manage dependencies.

## Quick Start

### Option 1: Use the activation script (Recommended)
```bash
activate_venv.bat
```

### Option 2: Manual activation
```bash
# Activate the virtual environment
venv\Scripts\activate

# Deactivate when done
deactivate
```

## What was installed

- **Python 3.14.3** - Latest Python version
- **discord.py 2.7.1** - Discord API library
- **aiohttp 3.13.4** - Async HTTP client/server
- **python-dotenv 1.2.2** - Environment variable management
- **pytest 9.0.2** - Testing framework
- **pytest-asyncio 1.3.0** - Async testing support
- **pytest-mock 3.15.1** - Mocking utilities

## Running the bot

After activating the virtual environment:
```bash
python run.py
```

## Notes

- The virtual environment is located in the `venv/` directory
- All dependencies are installed within the virtual environment
- No system-wide Python packages were modified
- Use `pip install <package>` to add new packages to the virtual environment
