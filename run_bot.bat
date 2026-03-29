@echo off
echo Starting Discord Book Bot...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your Discord bot token.
    echo.
    pause
    exit /b 1
)

REM Run the bot
echo Starting bot...
python bot.py

pause
