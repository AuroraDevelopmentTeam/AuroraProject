from core.embeds import construct_error_embed
import nextcord
from nextcord import Asset


def construct_error_forbidden_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text=f"error: FORBIDDEN\n discord #403")
    return embed


def construct_error_http_exception_embed(
        description: str, icon: Asset
) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text=f"error: HTTPException\n discord error")
    return embed


def construct_error_not_found_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text=f"error: NOT FOUND\n discord #404")
    return embed


def construct_error_limit_break_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text=f"error: LIMIT BREAK\nstatus-code: #A903")
    return embed


def construct_error_negative_value_embed(
        description: str, icon: Asset, value
) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(
        icon_url=icon,
        text=f"error: NOT POSITIVE/NOT INT VALUE\nvalue: {value}\nstatus-code: #A243",
    )
    return embed


def construct_error_bot_user_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(
        icon_url=icon,
        text=f"error: bot user\nstatus-code: #A003 ",
    )
    return embed


def construct_error_self_choose_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(
        icon_url=icon,
        text=f"error: self_choose_error\nstatus-code: #A178 ",
    )
    return embed


def construct_error_not_enough_embed(
        description: str, icon: Asset, footer_text
) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text=footer_text)
    return embed


def construct_error_already_married_embed(
        description: str, icon: Asset
) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text="♪ ♪ ♪")
    return embed


def construct_error_not_married_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text="♪ ♪ ♪")
    return embed


def construct_clan_error_embed(
        description: str, icon: Asset
) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text=f"error: ClanError")
    return embed

def construct_error_no_voice_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(
        icon_url=icon,
        text=f"error: no voice\nstatus-code: #A403 ",
    )
    return embed