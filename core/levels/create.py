from core.db_utils import execute_update


async def create_level_table() -> None:
    query = """
    CREATE TABLE IF NOT EXISTS levels (
        guild_id BIGINT, 
        user_id BIGINT, 
        level INTEGER, 
        exp INTEGER
    )
    """
    await execute_update(query)

async def create_level_config_table() -> None:
    query = """
    CREATE TABLE IF NOT EXISTS levels_config (
        guild_id BIGINT, 
        min_exp_per_message INTEGER, 
        max_exp_per_message INTEGER, 
        level_up_messages_state BOOLEAN
    )
    """
    await execute_update(query)

async def create_level_channels_config_table() -> None:
    query = """
    CREATE TABLE IF NOT EXISTS level_channels_config (
        guild_id BIGINT, 
        channel_id BIGINT, 
        enabled BOOL
    )
    """
    await execute_update(query)








