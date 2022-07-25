import nextcord
from nextcord import Asset
from config import settings
from nextcord.ext import commands
from core.locales.getters import get_msg_from_locale_by_key

DEFAULT_BOT_COLOR = settings["default_color"]


def construct_error_embed(description: str) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, description=description)
    return embed


def construct_basic_embed(name: str, value: str, footer_text: str, footer_url: Asset) -> nextcord.Embed:
    name = name.capitalize()
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    embed.add_field(name=name, value=value)
    embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed


def construct_long_embed(title: str, thumbnail_url: Asset, footer_text: str,
                         footer_url: Asset, name_list: list, value_list: list, inline: bool) -> nextcord.Embed:
    title = title.capitalize()
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, title=title)
    embed.set_footer(text=footer_text, icon_url=footer_url)
    embed.set_thumbnail(url=thumbnail_url)
    if len(name_list) == len(value_list):
        for name, value in zip(name_list, value_list):
            embed.add_field(name=name, value=value, inline=inline)
    return embed


def construct_top_embed(title: str, top_list: list, footer_text: str, footer_url: Asset,
                        currency_symbol=None, guild=None) -> nextcord.Embed:
    if guild is not None:
        msg = get_msg_from_locale_by_key(guild.id, "price")
    title = title.capitalize()
    counter = 0
    users = []
    for row in top_list:
        counter += 1
        if currency_symbol is not None:
            if guild is not None:
                msg = get_msg_from_locale_by_key(guild.id, "price")
                users.append(f"**{counter}** • {row[0]}\n> {msg} **{row[1]}** {currency_symbol}\n")
            else:
                users.append(f"**{counter}** • {row[0]}\n> **{row[1]}** {currency_symbol}\n")
        else:
            users.append(f"**{counter}** • {row[0]}\n> {row[1]}\n")
    if len(users) > 0:
        description = ' '.join([user for user in users])
    else:
        description = '...'
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, title=title, description=description)
    embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed
