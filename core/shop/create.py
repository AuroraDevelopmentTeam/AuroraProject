from core.db_utils import execute_update


async def create_shop_table() -> None:
    await execute_update(
        """CREATE TABLE IF NOT EXISTS shop (
        guild_id BIGINT, role_id BIGINT, cost INTEGER
    )"""
    )


async def create_custom_shop_table() -> None:
    await execute_update(
        """CREATE TABLE IF NOT EXISTS custom_shop ( guild_id BIGINT, role_id BIGINT, cost INTEGER, 
        owner_id BIGINT, created INTEGER, expiration_date INTEGER, bought INTEGER ) """
    )


async def create_custom_shop_config_table() -> None:
    await execute_update(
        """CREATE TABLE IF NOT EXISTS custom_shop_config (guild_id BIGINT, enabled BOOL, role_create_cost INTEGER ) """
    )
