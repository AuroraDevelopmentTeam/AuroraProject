from core.db_utils import execute_update


async def create_tickets_config_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS tickets_config (
        guild_id BIGINT, ticket_category INTEGER, ticket_archive INTEGER, ticket_support INTEGER
    )"""
    )