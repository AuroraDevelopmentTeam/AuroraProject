from core.db_utils import execute_update


async def update_ticket_category(guild_id: int, ticket_category: int) -> None:
    sql = "UPDATE tickets_config SET ticket_category = ? WHERE guild_id = ?"
    values = (ticket_category, guild_id)
    await execute_update(sql, values)


async def update_ticket_archive(guild_id: int, ticket_archive: int) -> None:
    sql = "UPDATE tickets_config SET ticket_archive = ? WHERE guild_id = ?"
    values = (ticket_archive, guild_id)
    await execute_update(sql, values)


async def update_ticket_support(guild_id: int, ticket_support: int) -> None:
    sql = "UPDATE tickets_config SET ticket_support = ? WHERE guild_id = ?"
    values = (ticket_support, guild_id)
    await execute_update(sql, values)
