import sqlite3
import typing
import sqlite3
import nextcord
from easy_pil import *
from core.embeds import DEFAULT_BOT_COLOR
import re


def create_goodbye_config() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS goodbye_config (guild_id INTEGER, goodbye_message_enabled BOOLEAN, 
    goodbye_message_channel INTEGER, goodbye_message_type TEXT, 
    goodbye_message_title TEXT, goodbye_message_description TEXT, goodbye_message_url TEXT )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_server_goodbye_embed(
    member: typing.Union[nextcord.Member, nextcord.User], guild: nextcord.Guild
) -> nextcord.Embed:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    goodbye_message_title = cursor.execute(
        f"SELECT goodbye_message_title FROM goodbye_config WHERE guild_id = {guild.id}"
    ).fetchone()[0]
    goodbye_message_description = cursor.execute(
        f"SELECT goodbye_message_description FROM goodbye_config WHERE guild_id = {guild.id}"
    ).fetchone()[0]
    goodbye_message_url = cursor.execute(
        f"SELECT goodbye_message_url FROM goodbye_config WHERE guild_id = {guild.id}"
    ).fetchone()[0]
    if "{member.mention}" in goodbye_message_title:
        goodbye_message_title = goodbye_message_title.replace(
            "{member.mention}", f"{member.mention}"
        )
    if "{member.tag}" in goodbye_message_title:
        goodbye_message_title = goodbye_message_title.replace(
            "{member.tag}", f"{member.tag}"
        )
    if "{member.created_at}" in goodbye_message_title:
        goodbye_message_title = goodbye_message_title.replace(
            "{member.created_at}", f"{member.created_at}"
        )
    if "{member.name}" in goodbye_message_title:
        goodbye_message_title = goodbye_message_title.replace(
            "{member.name}", f"{member.name}"
        )
    if "{member.id}" in goodbye_message_title:
        goodbye_message_title = goodbye_message_title.replace(
            "{member.id}", f"{member.id}"
        )
    if "{guild.id}" in goodbye_message_title:
        goodbye_message_title = goodbye_message_title.replace(
            "{guild.id}", f"{guild.id}"
        )
    if "{guild.name}" in goodbye_message_title:
        goodbye_message_title = goodbye_message_title.replace(
            "{guild.name}", f"{guild.name}"
        )
    if "{guild.id}" in goodbye_message_title:
        goodbye_message_title = goodbye_message_title.replace(
            "{guild.id}", f"{guild.id}"
        )
    if "{guild.members}" in goodbye_message_title:
        goodbye_message_title = goodbye_message_title.replace(
            "{guild.members}", f"{len(guild.members)}"
        )
    if "{member.mention}" in goodbye_message_description:
        goodbye_message_description = goodbye_message_description.replace(
            "{member.mention}", f"{member.mention}"
        )
    if "{member.tag}" in goodbye_message_description:
        goodbye_message_description = goodbye_message_description.replace(
            "{member.tag}", f"{member.tag}"
        )
    if "{member.created_at}" in goodbye_message_description:
        goodbye_message_description = goodbye_message_description.replace(
            "{member.created_at}", f"{member.created_at}"
        )
    if "{member.name}" in goodbye_message_description:
        goodbye_message_description = goodbye_message_description.replace(
            "{member.name}", f"{member.name}"
        )
    if "{member.id}" in goodbye_message_description:
        goodbye_message_description = goodbye_message_description.replace(
            "{member.id}", f"{member.id}"
        )
    if "{guild.id}" in goodbye_message_description:
        goodbye_message_description = goodbye_message_description.replace(
            "{guild.id}", f"{guild.id}"
        )
    if "{guild.name}" in goodbye_message_description:
        goodbye_message_description = goodbye_message_description.replace(
            "{guild.name}", f"{guild.name}"
        )
    if "{guild.id}" in goodbye_message_description:
        goodbye_message_description = goodbye_message_description.replace(
            "{guild.id}", f"{guild.id}"
        )
    if "{guild.members}" in goodbye_message_description:
        goodbye_message_description = goodbye_message_description.replace(
            "{guild.members}", f"{len(guild.members)}"
        )
    list_of_channels = [
        t for t in goodbye_message_description.split() if t.startswith("#")
    ]
    for channel in list_of_channels:
        if channel.isdigit() is True:
            really_channel = nextcord.utils.get(guild.text_channels, id=channel[1:])
            goodbye_message_description = goodbye_message_description.replace(
                channel, really_channel.mention
            )
        else:
            really_channel = nextcord.utils.get(guild.text_channels, name=channel[1:])
            goodbye_message_description = goodbye_message_description.replace(
                channel, really_channel.mention
            )
    db.commit()
    cursor.close()
    db.close()
    embed = nextcord.Embed(
        color=DEFAULT_BOT_COLOR,
        title=f"{goodbye_message_title}",
        description=f"{goodbye_message_description}",
    )
    embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
    embed.set_thumbnail(url=member.display_avatar)
    embed.set_image(url=goodbye_message_url)
    return embed


def create_goodbye_card(member) -> nextcord.File:
    background = Editor(Canvas((900, 300), color="#141414"))
    profile_picture = load_image(str(member.display_avatar))
    profile = Editor(profile_picture).resize((150, 150)).circle_image()
    larger_font = Font.montserrat(size=35)
    font = Font.montserrat(size=25)

    card_right_shape = [(650, 0), (750, 300), (900, 300), (900, 0)]

    background.polygon(card_right_shape, color="#FFFFFF")
    card_right_shape = [(750, 0), (550, 300), (900, 300), (900, 0)]
    background.polygon(card_right_shape, color="#FFFFFF")
    background.paste(profile, (30, 30))
    background.text((200, 40), str(member), font=larger_font, color="#FFFFFF")
    background.rectangle((200, 100), width=350, height=2, fill="#FFFFFF")
    background.text((200, 130), f"{member.guild.name}", font=font, color="#FFFFFF")
    background.rectangle((200, 190), width=350, height=2, fill="#FFFFFF")
    background.text(
        (300, 220), f"№{len(member.guild.members)}", font=larger_font, color="#FFFFFF"
    )
    file = nextcord.File(fp=background.image_bytes, filename="levelcard.png")
    return file
