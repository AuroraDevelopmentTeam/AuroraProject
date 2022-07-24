import sqlite3
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random

from easy_pil import *
import nextcord
from nextcord.ui import View, Button

from core.embeds import DEFAULT_BOT_COLOR
from core.locales.getters import get_msg_from_locale_by_key
from core.marriage.getters import get_user_love_description, get_user_marry_date, get_family_money
from core.money.getters import get_guild_currency_symbol


def create_marriage_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS marriage (
        guild_id INTERGER, user_id INTERGER, pair_id INTERGER, like_id INTERGER, 
        divorces INTERGER, love_description TEXT, date TEXT, family_money INTERGER)""")
    db.commit()
    cursor.close()
    db.close()
    return


def create_gifts_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS gifts (
        guild_id INTERGER, user_id INTERGER, gift_1 INTERGER, gift_2 INTERGER, gift_3 INTERGER, 
        gift_4 INTERGER, gift_5 INTERGER, gift_6 INTERGER, gift_7 INTERGER, gift_8 INTERGER, gift_9 INTERGER, 
        gift_10 INTERGER, gift_price INTERGER)""")
    db.commit()
    cursor.close()
    db.close()
    return


def create_marry_embed(name: str, guild_id: int, author: nextcord.Member, pair: nextcord.Member) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    marry = get_msg_from_locale_by_key(guild_id, name)
    marry_answer = get_msg_from_locale_by_key(guild_id, f"{name}_answer")
    embed.add_field(name=name.capitalize(),
                    value=f'{author.mention} {marry} {pair.mention} {marry_answer}',
                    inline=False)
    return embed


def create_marry_yes_embed(guild_id: int, author: nextcord.Member, pair: nextcord.Member) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    marry = get_msg_from_locale_by_key(guild_id, f"marry_yes")
    marry_answer = get_msg_from_locale_by_key(guild_id, f"marry_yes_answer")
    embed.add_field(name=marry,
                    value=f'{author.mention}+{pair.mention} {marry_answer}',
                    inline=False)
    return embed


def create_marry_no_embed(guild_id: int, author: nextcord.Member, pair: nextcord.Member) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    marry = get_msg_from_locale_by_key(guild_id, f"marry_no")
    marry_answer = get_msg_from_locale_by_key(guild_id, f"marry_no_answer")
    embed.add_field(name=marry,
                    value=f'{author.mention} {marry_answer} {pair.mention}',
                    inline=False)
    return embed


def create_love_card(avatar_1, avatar_2) -> nextcord.File:
    background = Editor(f'./assets/couple_card_{str(random.randint(1, 4))}.png').resize((800, 450))
    profile = Editor(avatar_1).resize((150, 150)).circle_image()
    background.paste(profile, (100, 180))
    heart = Editor(f'./assets/heart.png').resize((75, 75))
    background.paste(heart, (375, 205))
    profile = Editor(avatar_2).resize((150, 150)).circle_image()
    background.paste(profile, (550, 180))
    file = nextcord.File(fp=background.image_bytes, filename="lovecard.png")
    return file


def create_love_profile_embed(name: str, guild_id: int, user: nextcord.Member, pair: nextcord.Member) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    love_description = get_user_love_description(guild_id, user.id)
    love_date = get_user_marry_date(guild_id, user.id)
    family_money = get_family_money(guild_id, user.id)

    embed.add_field(name=name.capitalize(), value=f"{user.mention} <a:emoji_20:996467596851417089> {pair.mention}",
                    inline=False)
    field_name = get_msg_from_locale_by_key(guild_id, "love_description")
    embed.add_field(name=field_name, value=f"```{love_description}```", inline=False)
    currency_symbol = get_guild_currency_symbol(guild_id)
    field_name = get_msg_from_locale_by_key(guild_id, "love_money")
    embed.add_field(name=field_name, value=f"__**{family_money}**__ {currency_symbol}", inline=True)
    field_name = get_msg_from_locale_by_key(guild_id, "love_date")
    embed.add_field(name=field_name, value=f"**{love_date}**", inline=True)
    requested = get_msg_from_locale_by_key(guild_id, 'requested_by')
    embed.set_footer(text=f'{requested} {user}', icon_url=user.display_avatar)
    embed.set_image(url="attachment://lovecard.png")
    return embed
