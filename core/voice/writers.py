from core.db_utils import execute_update
from core.checkers import is_guild_id_in_table


async def write_in_voice_private_config_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("voice_private_config", guild.id) is False:
            sql = (
                "INSERT INTO voice_private_config(guild_id, voice_creation_room_id, voice_controller_msg_id) VALUES ("
                "%s, %s, %s) "
            )
            val = (guild.id, 0, 0)
            await execute_update(sql, val)
