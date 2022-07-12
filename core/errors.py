from core.embeds import construct_error_embed
import nextcord
from nextcord import Asset


def construct_error_forbidden_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text=f'error status code #403')
    return embed
