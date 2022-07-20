import sqlite3
from easy_pil import *
import nextcord

from core.embeds import construct_basic_embed
from core.checkers import is_guild_id_in_table, is_user_in_table


def create_level_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS levels (
        guild_id INTERGER, user_id INTERGER, level INTERGER, exp INTERGER
    )""")
    db.commit()
    cursor.close()
    db.close()
    return


def create_level_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS levels_config (
        guild_id INTERGER, min_exp_per_message INTERGER, max_exp_per_message INTERGER, level_up_messages_state BOOLEAN
    )""")
    db.commit()
    cursor.close()
    db.close()
    return


def create_card(user, user_level: int, user_exp: int, exp_to_next_level: int) -> nextcord.File:
    percentage = int(((user_exp * 100) / exp_to_next_level))
    background = Editor(Canvas((900, 300), color="#141414"))
    profile_picture = load_image(str(user.avatar.url))
    profile = Editor(profile_picture).resize((150, 150)).circle_image()
    larger_font = Font.montserrat(size=35)
    font = Font.montserrat(size=30)

    card_right_shape = [(650, 0), (750, 300), (900, 300), (900, 0)]

    background.polygon(card_right_shape, color="#FFFFFF")
    background.paste(profile, (30, 30))
    background.bar((30, 220), max_width=650, height=40, percentage=100, color="#FFFFFF", radius=150)
    if percentage > 1:
        background.bar((30, 220), max_width=650, height=40, percentage=percentage, color="#5865F2", radius=20)
    background.text((200, 40), str(user), font=larger_font, color="#FFFFFF")
    background.rectangle((200, 100), width=350, height=2, fill="#FFFFFF")
    background.text((200, 130), f"Level - {user_level} | XP - {user_exp}/{exp_to_next_level}",
                    font=font, color="#FFFFFF")
    file = nextcord.File(fp=background.image_bytes, filename="levelcard.png")
    return file
