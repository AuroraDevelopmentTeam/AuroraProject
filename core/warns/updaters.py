from core.db_utils import execute_update


async def remove_warn_from_table(warn_id: int, guild_id: int, user_id: int) -> None:
    await execute_update(
        f"DELETE FROM warns WHERE warn_id = {warn_id} AND guild_id = {guild_id} AND user_id = {user_id}"
    )


async def update_warn_reason(guild_id: int, warn_id: int, warn_reason: str):
    sql = "UPDATE warns SET warn_reason = %s WHERE guild_id = %s AND warn_id = %s"
    values = (warn_reason, guild_id, warn_id)
    await execute_update(sql, values)
