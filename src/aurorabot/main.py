import asyncio
import sys
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from aurorabot.bot import AuroraBot


def main():
    """Main entry point for the bot."""
    bot = AuroraBot()
    bot.run_bot()


if __name__ == "__main__":
    main() 