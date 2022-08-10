from core.embeds import construct_error_embed
import nextcord
from nextcord import Asset


def construct_error_forbidden_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text=f"error status code #403")
    return embed


def construct_error_http_exception_embed(
    description: str, icon: Asset
) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text=f"error: HTTPException")
    return embed


def construct_error_limit_break_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(
        icon_url=icon, text=f"error: LIMIT BREAK|TOO MANY ARGS|ARGUMENT IS TOO BIG"
    )
    return embed


def construct_error_negative_value_embed(
    description: str, icon: Asset, value
) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(
        icon_url=icon,
        text=f"error: NOT POSITIVE/NOT INT VALUE\nnegative value: {value}",
    )
    return embed


def construct_error_bot_user_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(
        icon_url=icon,
        text=f"error: bot user\n this command can't be executed with bot user, it will indicate to "
        f"ValueError ",
    )
    return embed


def construct_error_self_choose_embed(description: str, icon: Asset) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(
        icon_url=icon,
        text=f"error: bot user\n this command can't be executed with bot user, it will indicate to "
        f"ValueError ",
    )
    return embed


def construct_error_not_enough_embed(
    description: str, icon: Asset, footer_text
) -> nextcord.Embed:
    embed = construct_error_embed(description)
    embed.set_footer(icon_url=icon, text=footer_text)
    return embed
