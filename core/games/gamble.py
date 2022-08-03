import random

import nextcord
from nextcord import Asset

from core.embeds import DEFAULT_BOT_COLOR


def perform_strikes() -> tuple:
    user_strikes = random.randint(1, 18)
    bot_strikes = random.randint(3, 18)
    return user_strikes, bot_strikes


def compare_strikes(user_strikes: int, bot_strikes: int) -> bool:
    if user_strikes > bot_strikes:
        return True
    elif user_strikes == bot_strikes:
        return None
    else:
        return False


def approximate_bet(bet, state) -> tuple:
    if state is True:
        percentage = random.randint(50, 100) / 100
        bet *= percentage
        return percentage, bet
    if state is None:
        return 0, bet
    if state is False:
        percentage = random.randint(0, 80) / 100
        bet *= percentage
        return percentage, bet


def get_game_state(state) -> str:
    if state is True:
        return "**Player** win"
    if state is None:
        return "**Draw**"
    if state is False:
        return "**Bot** win"


def create_gamble_embed(
    state,
    game_state: str,
    percentage: int,
    user_strikes: int,
    bot_strikes: int,
    footer_text: str,
    footer_url: Asset,
) -> nextcord.Embed:
    embed = nextcord.Embed(
        title="Gamble", color=DEFAULT_BOT_COLOR, description=game_state
    )
    embed.add_field(
        name="User strikes", value=f"value **{user_strikes}/18**", inline=True
    )
    embed.add_field(
        name="Bot strikes", value=f"value **{bot_strikes}/18**", inline=True
    )
    if state is not None:
        embed.add_field(
            name="Percentage", value=f"```{percentage*100}%```", inline=False
        )
    embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed
