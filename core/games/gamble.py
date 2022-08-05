import random

import nextcord
from nextcord import Asset

from core.embeds import DEFAULT_BOT_COLOR
from core.locales.getters import get_msg_from_locale_by_key


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


def get_game_state(state, user: nextcord.Member, client, guild_id: int) -> str:
    if state is True:
        return f'{user.mention} **{get_msg_from_locale_by_key(guild_id, "win")}**'
    if state is None:
        return f'**{get_msg_from_locale_by_key(guild_id, "draw")}**'
    if state is False:
        return f'{client.user.mention} **{get_msg_from_locale_by_key(guild_id, "win")}**'


def create_gamble_embed(
    state,
    game_state: str,
    percentage: int,
    user_strikes: int,
    bot_strikes: int,
    footer_text: str,
    footer_url: Asset,
    guild_id: int
) -> nextcord.Embed:
    title = get_msg_from_locale_by_key(guild_id, "gamble")
    bot_strikes_msg = get_msg_from_locale_by_key(guild_id, "bot_strikes")
    user_strikes_msg = get_msg_from_locale_by_key(guild_id, "user_strikes")
    percentage_msg = get_msg_from_locale_by_key(guild_id, "percentage")
    value_msg = get_msg_from_locale_by_key(guild_id, "value")
    embed = nextcord.Embed(
        title=title, color=DEFAULT_BOT_COLOR, description=game_state
    )
    embed.add_field(
        name=user_strikes_msg, value=f"{value_msg} **{user_strikes}/18**", inline=True
    )
    embed.add_field(
        name=bot_strikes_msg, value=f"{value_msg} **{bot_strikes}/18**", inline=True
    )
    if state is not None:
        embed.add_field(
            name=percentage_msg, value=f"```{percentage*100}%```", inline=False
        )
    embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed
