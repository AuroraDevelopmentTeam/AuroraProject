from ..db_utils import execute_update
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random

from easy_pil import *
import nextcord
from nextcord.ui import View, Button

from core.embeds import DEFAULT_BOT_COLOR
from core.locales.getters import get_msg_from_locale_by_key, localize_name
from core.marriage.getters import (
    get_user_love_description,
    get_user_marry_date,
    get_family_money,
    get_marriage_config_marriage_price,
)
from core.money.getters import get_guild_currency_symbol
from core.emojify import *


async def create_marriage_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS marriage (
        guild_id BIGINT, user_id BIGINT, pair_id INTEGER, like_id INTEGER, 
        divorces INTEGER, love_description TEXT, date TEXT, family_money INTEGER, loveroom_expire INTEGER, 
        loveroom_id INTEGER)"""
    )


async def create_marriage_config_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS marriage_config ( guild_id BIGINT, enable_loverooms BOOL, marriage_price 
        INTEGER, month_loveroom_price INTEGER, loveroom_category INTEGER) """
    )


async def create_gifts_table() -> None:
    await execute_update(
        f"""CREATE TABLE IF NOT EXISTS gifts (
        guild_id BIGINT, user_id BIGINT, gift_1 INTEGER, gift_2 INTEGER, gift_3 INTEGER, 
        gift_4 INTEGER, gift_5 INTEGER, gift_6 INTEGER, gift_7 INTEGER, gift_8 INTEGER, gift_9 INTEGER, 
        gift_10 INTEGER, gift_price INTEGER)"""
    )


async def add_column(guilds) -> None:
    await execute_update(
        """ALTER TABLE marriage 
        ADD COLUMN 'loveroom_expire' 'integer'"""
    )
    for guild in guilds:
        for member in guild.members:
            if not member.bot:
                if await is_user_in_table("marriage", guild.id, member.id) is True:
                    sql = (
                        "INSERT INTO marriage(loveroom_expire, loveroom_id) VALUES (?, ?)"
                            )
                    val = (0, 0)
                    await execute_update(sql, val)

async def create_marry_embed(
        name: str, guild_id: int, author: nextcord.Member, pair: nextcord.Member
) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    marry = get_msg_from_locale_by_key(guild_id, name)
    marry_answer = get_msg_from_locale_by_key(guild_id, f"{name}_answer")
    currency_symbol = await get_guild_currency_symbol(guild_id)
    marriage_price = await get_marriage_config_marriage_price(guild_id)
    embed.add_field(
        name=f"{MARRY} {name.capitalize()}",
        value=f"{author.mention} {marry} {pair.mention} {marry_answer} **{marriage_price}** {currency_symbol}",
        inline=False,
    )
    return embed


def create_marry_yes_embed(
        guild_id: int, author: nextcord.Member, pair: nextcord.Member
) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    marry = get_msg_from_locale_by_key(guild_id, f"marry_yes")
    marry_answer = get_msg_from_locale_by_key(guild_id, f"marry_yes_answer")
    embed.add_field(
        name=f"{MARRY} {marry}",
        value=f"{author.mention}+{pair.mention} {marry_answer}",
        inline=False,
    )
    return embed


def create_marry_no_embed(
        guild_id: int, author: nextcord.Member, pair: nextcord.Member
) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    marry = get_msg_from_locale_by_key(guild_id, f"marry_no")
    marry_answer = get_msg_from_locale_by_key(guild_id, f"marry_no_answer")
    embed.add_field(
        name=marry,
        value=f"{author.mention} {marry_answer} {pair.mention}",
        inline=False,
    )
    return embed


def create_love_card(avatar_1, avatar_2) -> nextcord.File:
    background = Editor(f"./assets/couple_card_{str(random.randint(1, 4))}.png").resize(
        (800, 450)
    )
    profile = Editor(avatar_1).resize((150, 150)).circle_image()
    background.paste(profile, (100, 180))
    heart = Editor(f"./assets/heart.png").resize((75, 75))
    background.paste(heart, (375, 205))
    profile = Editor(avatar_2).resize((150, 150)).circle_image()
    background.paste(profile, (550, 180))
    file = nextcord.File(fp=background.image_bytes, filename="lovecard.png")
    return file


async def create_love_profile_embed(
        name: str, guild_id: int, user: nextcord.Member, pair: nextcord.Member
) -> nextcord.Embed:
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
    love_description = await get_user_love_description(guild_id, user.id)
    love_date = await get_user_marry_date(guild_id, user.id)
    family_money = await get_family_money(guild_id, user.id)
    name = localize_name(guild_id, name).capitalize()
    name = name.replace("_", " ")
    embed.add_field(
        name=f"{MARRY} {name}",
        value=f"{user.mention} <a:emoji_20:996467596851417089> {pair.mention}",
        inline=False,
    )
    field_name = get_msg_from_locale_by_key(guild_id, "love_description")
    embed.add_field(
        name=f"{HEARTS_SCROLL} {field_name}",
        value=f"```{love_description}```",
        inline=False,
    )
    currency_symbol = await get_guild_currency_symbol(guild_id)
    field_name = get_msg_from_locale_by_key(guild_id, "love_money")
    embed.add_field(
        name=f"{PIGBANK} {field_name}",
        value=f"__**{family_money}**__ {currency_symbol}",
        inline=True,
    )
    field_name = get_msg_from_locale_by_key(guild_id, "love_date")
    embed.add_field(
        name=f"{HEARTS_MANY} {field_name}", value=f"**{love_date}**", inline=True
    )
    requested = get_msg_from_locale_by_key(guild_id, "requested_by")
    embed.set_footer(text=f"{requested} {user}", icon_url=user.display_avatar)
    embed.set_image(url="attachment://lovecard.png")
    return embed
