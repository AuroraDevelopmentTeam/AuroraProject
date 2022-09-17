import sqlite3

import nextcord

from core.embeds import DEFAULT_BOT_COLOR
from core.emojify import TEAM, LOCK, UNLOCK, PEN, KICK, YES, NO, CROWN, MUTE, MICROPHONE


def create_voice_private_config_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS voice_private_config (
        guild_id INTEGER, voice_creation_room_id INTEGER, voice_controller_msg_id INTEGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return


def create_button_menu_embed() -> nextcord.Embed:
    embed = nextcord.Embed(
        title="Управление приватной комнатой",
        description=f"""\n
        {PEN} - **изменить** название комнаты\n
        {TEAM} - **изменить** кол-во слотов\n
        {LOCK} - **закрыть** комнату для всех\n
        {UNLOCK} - **открыть** комнату для всех\n
        {KICK} - **выгнать** пользователя с комнаты\n
        {YES} - **дать доступ пользователю** в комнату\n
        {NO} - **забрать доступ пользователю** в комнату\n
        {MICROPHONE} - **размутить** пользователя\n
        {MUTE} - **замутить** пользователя\n
        {CROWN} - **передать владение** комнатой\n
    """,
        colour=DEFAULT_BOT_COLOR
    )
    return embed


async def react_on_private_room_menu_button(client, interaction: nextcord.Interaction, custom_id):
    pass