#!/usr/bin/env python3
"""
Check if the environment is properly set up for the Discord Book Bot
"""

import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Please copy .env.example to .env and add your Discord token")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'DISCORD_TOKEN =your_discord_bot_token_here' in content:
            print("❌ Discord token not set in .env file")
            return False
    
    print("✅ .env file found and configured")
    return True

def check_dependencies():
    """Check if required dependencies can be imported"""
    required_modules = [
        'discord',
        'googlesearch',
        'requests',
        'bs4',
        'dotenv'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            if module == 'bs4':
                import bs4
                print(f"✅ {module} (beautifulsoup4)")
            else:
                __import__(module)
                print(f"✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module} not installed")
    
    if missing_modules:
        print(f"\n   To install missing modules: pip install -r requirements.txt")
        return False
    
    return True

def main():
    print("🔍 Checking Discord Book Bot setup...\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Dependencies", check_dependencies)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"Checking {check_name}:")
        if not check_func():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 All checks passed! You can run the bot with: python bot.py")
    else:
        print("❌ Some checks failed. Please fix the issues above before running the bot.")
        print("\n💡 Need help? Check SETUP.md for detailed instructions.")

if __name__ == "__main__":
    main()
