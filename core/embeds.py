import nextcord
from nextcord import Asset
from config import settings

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
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, title=title)
    embed.set_footer(text=footer_text, icon_url=footer_url)
    embed.set_thumbnail(url=thumbnail_url)
    if len(name_list) == len(value_list):
        for name, value in zip(name_list, value_list):
            embed.add_field(name=name, value=value, inline=inline)
    return embed


def construct_top_embed():
    pass
