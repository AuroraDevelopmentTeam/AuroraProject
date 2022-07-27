import typing
import sqlite3
import nextcord

from easy_pil import *
from core.embeds import DEFAULT_BOT_COLOR
import re


def create_on_nitro_config() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS on_nitro_config (guild_id INTERGER, nitro_message_enabled BOOLEAN, 
    nitro_message_channel INTERGER, 
    nitro_message_title TEXT, nitro_message_description TEXT, nitro_message_url TEXT )""")
    db.commit()
    cursor.close()
    db.close()
    return


def create_server_nitro_embed(member: typing.Union[nextcord.Member, nextcord.User], guild: nextcord.Guild) -> nextcord.Embed:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    welcome_message_title = \
        cursor.execute(f"SELECT nitro_message_title FROM on_nitro_config WHERE guild_id = {guild.id}").fetchone()[0]
    welcome_message_description = \
        cursor.execute(
            f"SELECT nitro_message_description FROM on_nitro_config WHERE guild_id = {guild.id}").fetchone()[0]
    welcome_message_url = \
        cursor.execute(
            f"SELECT nitro_message_url FROM on_nitro_config WHERE guild_id = {guild.id}").fetchone()[0]
    if "{member.mention}" in welcome_message_title:
        welcome_message_title = welcome_message_title.replace("{member.mention}", f"{member.mention}")
    if "{member.tag}" in welcome_message_title:
        welcome_message_title = welcome_message_title.replace("{member.tag}", f"{member.tag}")
    if "{member.created_at}" in welcome_message_title:
        welcome_message_title = welcome_message_title.replace("{member.created_at}", f"{member.created_at}")
    if "{member.name}" in welcome_message_title:
        welcome_message_title = welcome_message_title.replace("{member.name}", f"{member.name}")
    if "{member.id}" in welcome_message_title:
        welcome_message_title = welcome_message_title.replace("{member.id}", f"{member.id}")
    if "{guild.id}" in welcome_message_title:
        welcome_message_title = welcome_message_title.replace("{guild.id}", f"{guild.id}")
    if "{guild.name}" in welcome_message_title:
        welcome_message_title = welcome_message_title.replace("{guild.name}", f"{guild.name}")
    if "{guild.id}" in welcome_message_title:
        welcome_message_title = welcome_message_title.replace("{guild.id}", f"{guild.id}")
    if "{guild.members}" in welcome_message_title:
        welcome_message_title = welcome_message_title.replace("{guild.members}", f"{len(guild.members)}")
    if "{member.mention}" in welcome_message_description:
        welcome_message_description = welcome_message_description.replace("{member.mention}", f"{member.mention}")
    if "{member.tag}" in welcome_message_description:
        welcome_message_description = welcome_message_description.replace("{member.tag}", f"{member.tag}")
    if "{member.created_at}" in welcome_message_description:
        welcome_message_description = welcome_message_description.replace("{member.created_at}", f"{member.created_at}")
    if "{member.name}" in welcome_message_description:
        welcome_message_description = welcome_message_description.replace("{member.name}", f"{member.name}")
    if "{member.id}" in welcome_message_description:
        welcome_message_description = welcome_message_description.replace("{member.id}", f"{member.id}")
    if "{guild.id}" in welcome_message_description:
        welcome_message_description = welcome_message_description.replace("{guild.id}", f"{guild.id}")
    if "{guild.name}" in welcome_message_description:
        welcome_message_description = welcome_message_description.replace("{guild.name}", f"{guild.name}")
    if "{guild.id}" in welcome_message_description:
        welcome_message_description = welcome_message_description.replace("{guild.id}", f"{guild.id}")
    if "{guild.members}" in welcome_message_description:
        welcome_message_description = welcome_message_description.replace("{guild.members}", f"{len(guild.members)}")
    list_of_channels = [t for t in welcome_message_description.split() if t.startswith('#')]
    for channel in list_of_channels:
        if channel.isdigit() is True:
            really_channel = nextcord.utils.get(guild.text_channels, id=channel[1:])
            welcome_message_description = welcome_message_description.replace(channel, really_channel.mention)
        else:
            really_channel = nextcord.utils.get(guild.text_channels, name=channel[1:])
            welcome_message_description = welcome_message_description.replace(channel, really_channel.mention)
    db.commit()
    cursor.close()
    db.close()
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, title=f"{welcome_message_title}",
                           description=f"{welcome_message_description}")
    embed.set_footer(text=f'{guild.name}', icon_url=guild.icon)
    embed.set_thumbnail(url=member.display_avatar)
    embed.set_image(url=welcome_message_url)
    return embed