from core.db_utils import fetch_one


async def get_ticket_category(guild_id: int) -> int:
    ticket_category = await fetch_one(
        f"SELECT ticket_category FROM tickets_config WHERE guild_id = {guild_id}"
    )
    return ticket_category[0]


async def get_ticket_archive(guild_id: int) -> int:
    ticket_archive = await fetch_one(
        f"SELECT ticket_archive FROM tickets_config WHERE guild_id = {guild_id}"
    )
    return ticket_archive[0]


async def get_ticket_support(guild_id: int) -> int:
    ticket_support = await fetch_one(
        f"SELECT ticket_support FROM tickets_config WHERE guild_id = {guild_id}"
    )
    return ticket_support[0]
