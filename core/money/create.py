from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps

from easy_pil import *
import sqlite3
import nextcord

from core.money.getters import get_user_balance
from core.locales.getters import get_msg_from_locale_by_key, localize_name
from core.checkers import is_guild_id_in_table, is_user_in_table
from core.embeds import DEFAULT_BOT_COLOR
from core.emojify import CREDIT_CARD


def create_money_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS money (
        guild_id INTEGER, user_id INTEGER, balance INTEGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_money_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS money_config (
        guild_id INTEGER, guild_currency TEXT, guild_payday_amount INTEGER, 
        guild_starting_balance INTEGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_role_money_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS roles_money (
        guild_id INTEGER, role_id INTEGER, income INTEGER, cooldown TEXT
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_chat_money_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS chat_money_config (
        guild_id INTEGER, min_msg_income INTEGER, max_msg_income INTEGER, msg_cooldown INTEGER, 
        min_voice_income INTEGER, max_voice_income INTEGER, voice_minutes_for_money INTEGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_money_channels_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS money_channels_config (
        guild_id INTEGER, channel_id INTEGER, enabled BOOL)"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_user_money_card(
    name, author, user, avatar, guild_id
) -> tuple[nextcord.File, nextcord.Embed]:
    background = Editor("./assets/credit_card.png")
    profile = Editor(avatar).resize((250, 250)).circle_image()
    larger_font = Font.montserrat(size=35)
    font = Font.montserrat(size=30)
    background.paste(profile, (760, 390))
    balance = get_user_balance(guild_id, user.id)
    background.text((150, 530), str(user), font=font, color="#FFFFFF")
    background.text((400, 479.8), f"{balance}", font=larger_font, color="#FFFFFF")
    requested = get_msg_from_locale_by_key(guild_id, "requested_by")
    name = localize_name(guild_id, name).capitalize()
    embed = nextcord.Embed(
        color=DEFAULT_BOT_COLOR, title=f"{CREDIT_CARD} {name} - {user}"
    )
    embed.set_footer(icon_url=author.display_avatar, text=f"{requested} {author}")
    file = nextcord.File(fp=background.image_bytes, filename="balance_card.png")
    embed.set_image(url="attachment://balance_card.png")
    return file, embed
