from core.checkers import is_guild_id_in_table, is_user_in_table
from core.db_utils import execute_update


async def write_in_tickets_config_standart_values(guilds) -> None:
    for guild in guilds:
        if await is_guild_id_in_table("tickets_config", guild.id) is False:
            sql = (
                "INSERT INTO tickets_config(guild_id, ticket_category, "
                "ticket_archive, ticket_support) VALUES (?, ?, ?, ?)"
            )
            val = (guild.id, 0, 0, 0)
            await execute_update(sql, val)
