from ..db_utils import execute_update

async def create_bets_table() -> None:
    await execute_update(
        """CREATE TABLE IF NOT EXISTS bets (guild_id BIGINT, min_bet INTEGER, max_bet INTEGER) """
    )
