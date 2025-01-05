import sqlite3
from core.checkers import is_user_in_table

from ...db_utils import execute_update

async def create_duels_stats_money_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS duels (
        guild_id BIGINT, user_id BIGINT, duels_won INTEGER, games INTEGER, 
        best_attack INTEGER, most_won INTEGER, class TEXT, battle_page TEXT
    )"""
    )


async def write_in_duels_standart_values(guilds) -> None:
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if await is_user_in_table("duels", guild.id, member.id) is False:
                    sql = (
                        "INSERT INTO duels(guild_id, user_id, duels_won, games, "
                        "best_attack, most_won, class, battle_page) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                    )
                    val = (guild.id, member.id, 0, 0, 0, 0, "rat", "focused_punch")
                    await execute_update(sql, val)
