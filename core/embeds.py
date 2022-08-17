import nextcord
from nextcord import Asset
from config import settings
from nextcord.ext import commands
from core.locales.getters import get_msg_from_locale_by_key, localize_name
from core.emojify import CLOCK

DEFAULT_BOT_COLOR = settings["default_color"]


def construct_error_embed(description: str) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, description=description)
    return embed


def construct_basic_embed(
    name: str, value: str, footer_text: str, footer_url: Asset, guild_id: int
) -> nextcord.Embed:
    try:
        if name == 'timely':
            name = f"{localize_name(guild_id, name).capitalize()}"
            name = CLOCK + " " + name
        else:
            name = localize_name(guild_id, name)
            name = name.capitalize()
    except Exception as error:
        name = name
        print(error)
    name = name.replace("_", " ")
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    embed.add_field(name=name, value=value)
    embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed


def construct_long_embed(
    title: str,
    thumbnail_url: Asset,
    footer_text: str,
    footer_url: Asset,
    name_list: list,
    value_list: list,
    inline: bool,
) -> nextcord.Embed:
    title = title.capitalize()
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, title=title)
    embed.set_footer(text=footer_text, icon_url=footer_url)
    embed.set_thumbnail(url=thumbnail_url)
    if len(name_list) == len(value_list):
        for name, value in zip(name_list, value_list):
            embed.add_field(name=name, value=value, inline=inline)
    return embed


def construct_top_embed(
    title: str,
    top_list: list,
    footer_text: str,
    footer_url: Asset,
    currency_symbol=None,
    guild=None,
) -> nextcord.Embed:
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
                users.append(
                    f"**{counter}** • {row[0]}\n> {msg} **{row[1]}** {currency_symbol}\n"
                )
            else:
                users.append(
                    f"**{counter}** • {row[0]}\n> **{row[1]}** {currency_symbol}\n"
                )
        else:
            users.append(f"**{counter}** • {row[0]}\n> {row[1]}\n")
    if len(users) > 0:
        description = " ".join([user for user in users])
    else:
        description = "..."
    embed = nextcord.Embed(
        color=DEFAULT_BOT_COLOR, title=title, description=description
    )
    embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed


def construct_log(
    event_type: str,
    guild: nextcord.Guild,
    message: nextcord.Message = None,
    jump_url: bool = False,
    display_message: bool = True,
    message_channel: nextcord.TextChannel = None,
    user: nextcord.Member = None,
    before: nextcord.Message = None,
    after: nextcord.Message = None,
    role: nextcord.Role = None,
    role_before: nextcord.Role = None,
    role_after: nextcord.Role = None,
    channel=None,
    channel_before=None,
    channel_after=None,
) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, title=event_type)
    if message_channel is not None:
        embed.add_field(
            name="Channel",
            value=f"{message_channel.mention}\nID: **{message_channel.id}**",
            inline=False,
        )
    if user is not None:
        embed.add_field(
            name="User",
            value=f"{user.mention}\n`{user}`, ID: **{user.id}**",
            inline=False,
        )
        embed.set_thumbnail(url=f"{user.display_avatar}")
    if jump_url is True:
        embed.add_field(
            name="URL", value=f"[message]({message.jump_url})", inline=False
        )
    if message is not None and display_message is True:
        embed.add_field(name="Message", value=f"``{message.content}``", inline=False)
    if before is not None:
        embed.add_field(name="Before", value=f"``{before.content}``", inline=True)
    if after is not None:
        embed.add_field(name="After", value=f"``{after.content}``", inline=True)
    if role is not None:
        embed.add_field(
            name="Role",
            value=f"{role.mention}\n"
            f"ID: **{role.id}**, name: ``{role.name}``\n"
            f"Position: **{role.position}**, mentionable: **{role.mentionable}**\n"
            f"Permissions: **{role.permissions.value}**",
            inline=False,
        )
    if role_before is not None:
        embed.add_field(
            name="Before",
            value=f"``@{role_before.name}``, ``{role_before.color}``\n"
            f"Position: **{role_before.position}**, mentionable: "
            f"**{role_before.mentionable}**\n"
            f"Permissions: **{role_before.permissions.value}**",
            inline=True,
        )
    if role_after is not None:
        embed.add_field(
            name="After",
            value=f"{role_after.mention}\n``@{role_after.name}``, ``{role_after.color}``\n"
            f"Position: **{role_after.position}**, mentionable: "
            f"**{role_after.mentionable}**\n"
            f"Permissions: **{role_after.permissions.value}**",
            inline=True,
        )
    if channel is not None:
        embed.add_field(
            name="Channel", value=f"``{channel.name}``, {channel.mention}", inline=False
        )
    if channel_before is not None:
        embed.add_field(name="Before", value=f"``{channel_before.name}``", inline=True)
    if channel_after is not None:
        embed.add_field(
            name="After",
            value=f"``{channel_after.name}``, {channel_after.mention}\n"
            f"Changed roles: {channel_after.changed_roles} ",
            inline=True,
        )
    embed.set_footer(text=f"{guild.name}\nAURORA", icon_url=guild.icon)
    return embed
