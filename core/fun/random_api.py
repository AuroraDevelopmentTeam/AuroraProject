import nextcord

from core.locales.getters import localize_name
from core.embeds import DEFAULT_BOT_COLOR


def build_random_image_embed(title: str, link: str, guild_id) -> nextcord.Embed:
    name = localize_name(guild_id, title)
    name = name.capitalize()
    name = name.replace('_', ' ')
    embed = nextcord.Embed(title=name, color=DEFAULT_BOT_COLOR)
    embed.set_image(url=link)
    return embed
