import nextcord
from nextcord import Asset
from config import settings

DEFAULT_BOT_COLOR = settings["default_color"]


def construct_basic_embed(name: str, value: str, footer_text: str, footer_url: Asset):
    name = name.capitalize()
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    embed.add_field(name=name, value=value)
    embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed
