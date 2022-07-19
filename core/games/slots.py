import random

import nextcord

from core.money.getters import get_user_balance
from core.embeds import DEFAULT_BOT_COLOR

slot_emojis = ['<:1388purincherry:998435904756645949>', '<:5471koifish:998435906233053315>',
               '<:1181bunnyhappy:998435907763982386>', '<:9810aestheticflower:998286492269023354>',
               '<a:8293_Butterfly_White:998286778559627344>', '<a:whitecrown:998827454615519283>']


def spin_slots() -> list:
    result_row = []
    for _ in range(3):
        result_row.append(random.choice(slot_emojis))
    return result_row


def check_win_get_multiplier(row: list):
    if row[0] == row[1] and row[1] == row[2]:
        return True, 2
    elif row[0] == row[1] or row[1] == row[2] or row[2] == row[0]:
        return True, 1
    else:
        return False, 0


def unpack_slots_row(row: list) -> str:
    return f'**<** {row[0]} {row[1]} {row[2]} **>**'


def create_slots_embed(guild_id, user_id, footer_url: nextcord.Asset,
                       name: str, slots_row: list, game_state: str) -> nextcord.Embed:
    name = name.capitalize()
    users_balance = get_user_balance(guild_id, user_id)
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR,
                           description=f'**{name}**\n{game_state}\n{unpack_slots_row(slots_row)}')
    embed.set_footer(icon_url=footer_url, text=f'{users_balance}')
    return embed