from ..db_utils import execute_update
from core.checkers import is_guild_id_in_table
import json
from config import settings


async def create_locales_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS locales (
        guild_id BIGINT, locale TEXT
    )"""
    )
