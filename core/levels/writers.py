from ..db_utils import execute_update
from core.checkers import is_guild_id_in_table, is_user_in_table
from config import settings
from core.levels.getters import get_channel_level_state


async def write_in_levels_config_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("levels_config", guild.id) is False:
            sql = (
                "INSERT INTO levels_config(guild_id, min_exp_per_message, max_exp_per_message, "
                "level_up_messages_state) VALUES (%s, %s, %s, %s)"
            )
            val = (
                guild.id,
                settings["default_min_exp"],
                settings["default_max_exp"],
                settings["default_level_up_messages_state"],
            )
            await execute_update(sql, val)


async def write_in_levels_standart_values(guilds) -> None:
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if await is_user_in_table("levels", guild.id, member.id) is False:
                    sql = "INSERT INTO levels(guild_id, user_id, level, exp) VALUES (%s, %s, %s, %s)"
                    val = (guild.id, member.id, 1, 0)
                    await execute_update(sql, val)


async def write_channel_in_config(guild_id: int, channel_id: int, enabled: bool) -> None:
    if enabled is True:
        if await get_channel_level_state(guild_id, channel_id) is False:
            try:
                sql = f"DELETE FROM level_channels_config WHERE guild_id = {guild_id} AND channel_id = {channel_id}"
                await execute_update(sql)
            except:
                pass
    else:
        sql = "INSERT INTO level_channels_config(guild_id, channel_id, enabled) VALUES (%s, %s, %s)"
        val = (guild_id, channel_id, enabled)
        await execute_update(sql, val)
