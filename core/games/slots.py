import random

import nextcord

from core.locales.getters import get_msg_from_locale_by_key
from core.money.getters import get_user_balance
from core.embeds import DEFAULT_BOT_COLOR

slot_emojis = [
    "<:1388purincherry:998435904756645949>",
    "<:5471koifish:998435906233053315>",
    "<:1181bunnyhappy:998435907763982386>",
    "<:9810aestheticflower:998286492269023354>",
    "<a:8293_Butterfly_White:998286778559627344>",
    "<a:whitecrown:998827454615519283>",
    "<a:8243blackbat:999977356468965457>",
]

MULTIPLIERS_FOR_TWO_ROWS = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]

MULTIPLIERS_FOR_THREE_ROWS = [2.0, 2.1, 2.2, 2.3, 2.4, 2.5]


def spin_slots() -> list:
    result_row = []
    for _ in range(3):
        result_row.append(random.choice(slot_emojis))
    return result_row


def check_win_get_multiplier(row: list):
    if row[0] == row[1] and row[1] == row[2]:
        return True, random.choice(MULTIPLIERS_FOR_THREE_ROWS)
    elif row[0] == row[1] or row[1] == row[2] or row[2] == row[0]:
        return True, random.choice(MULTIPLIERS_FOR_TWO_ROWS)
    else:
        return False, 0


def unpack_slots_row(row: list) -> str:
    return f"**<** {row[0]} {row[1]} {row[2]} **>**"


def create_slots_embed(
    guild_id,
    user_id,
    footer_url: nextcord.Asset,
    name: str,
    slots_row: list,
    game_state: str,
) -> nextcord.Embed:
    name = name.capitalize()
    users_balance = get_user_balance(guild_id, user_id)
    additional_row = spin_slots()
    additional_row_2 = spin_slots()
    embed = nextcord.Embed(
        color=DEFAULT_BOT_COLOR,
        description=f"**{name}**\n{game_state}\n"
        f"**|** {additional_row[0]} {additional_row[1]} {additional_row[2]} **|**\n"
        f"{unpack_slots_row(slots_row)}\n"
        f"**|** {additional_row_2[0]} {additional_row_2[1]} {additional_row_2[2]} **|**",
    )
    msg = get_msg_from_locale_by_key(guild_id, "on_balance")
    embed.set_footer(icon_url=footer_url, text=f"{msg} {users_balance}")
    return embed
