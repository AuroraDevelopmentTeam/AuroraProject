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