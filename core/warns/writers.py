from core.db_utils import execute_update
import random

from core.checkers import is_warn_id_in_table


async def write_new_warn(guild_id, user_id, reason) -> None:
    warn_id = random.randint(1, 1000000000000000)
    while await is_warn_id_in_table("warns", warn_id, guild_id, user_id) is True:
        warn_id = random.randint(1, 1000000000000000)
    if await is_warn_id_in_table("warns", warn_id, guild_id, user_id) is False:
        sql = (
            "INSERT INTO warns(warn_id, guild_id, user_id, "
            "warn_reason) VALUES (?, ?, ?, ?)"
        )
        val = (warn_id, guild_id, user_id, reason)
        await execute_update(sql, val)
