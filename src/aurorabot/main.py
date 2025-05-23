import asyncio
import sys
from pathlib import Path

# Добавление директории src в путь Python
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from aurorabot.bot import AuroraBot


async def main():
    """Основная точка входа для бота."""
    bot = AuroraBot()
    try:
        await bot.start(bot.config.bot_config["token"])
    except KeyboardInterrupt:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main()) 