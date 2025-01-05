from ..db_utils import execute_update, fetch_one
from core.checkers import is_guild_id_in_table, is_user_in_table
from config import settings


async def write_in_honor_standart_values(guilds) -> None:
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if (
                    await fetch_one(
                        f"SELECT user_id FROM honor WHERE user_id = {member.id}"
                    )
                    is None
                ):
                    sql = "INSERT INTO honor(user_id, honor_level, honor_points) VALUES (%s, %s, %s)"
                    val = (member.id, 2, 0)
                    await execute_update(sql, val)
