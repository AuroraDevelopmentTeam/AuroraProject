import sqlite3

import nextcord

from core.embeds import DEFAULT_BOT_COLOR


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
        description="""\n
        🖊 - **изменить** название комнаты\n
        👥 - **изменить** кол-во слотов\n
        🔒 - **закрыть** комнату для всех\n
        🔓 - **открыть** комнату для всех\n
        🚪 - **выгнать** пользователя с комнаты\n
        ✔ - **дать доступ пользователю** в комнату\n
        ❌ - **забрать доступ пользователю** в комнату\n
        🔉 - **размутить** пользователя\n
        🔇 - **замутить** пользователя\n
        👑 - **передать владение** комнатой\n
    """,
        colour=DEFAULT_BOT_COLOR
    )
    return embed
