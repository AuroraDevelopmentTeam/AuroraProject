import random

import sqlite3
import nextcord

from core.locales.getters import get_msg_from_locale_by_key
from core.embeds import DEFAULT_BOT_COLOR
from core.money.getters import get_user_balance


def create_emotion_embed(
        guild_id: int,
        emotion_name: str,
        emotion_type: str,
        author: nextcord.Member,
        gifs: list,
        is_free: bool = True,
        cost=0,
        user: nextcord.Member = None,
        author_msg: str = None,
) -> nextcord.Embed:
    emotion_name = get_msg_from_locale_by_key(guild_id, f"emotion_{emotion_name}")
    if user is not None:
        if emotion_type == "positive":
            description = f"**{emotion_name}**\n{author.mention} **✧** {user.mention}"
            moji = "(ᴖ◡ᴖ)♪"
        elif emotion_type == "neutral":
            description = f"**{emotion_name}**\n{author.mention} **○** {user.mention}"
            moji = random.choice(
                ["┐(￣ヮ￣)┌", "(•ิ_•ิ)?", "	ლ(ಠ_ಠ ლ)", "	(・_・ヾ", "(↼_↼)"]
            )
        elif emotion_type == "angry":
            description = f"**{emotion_name}**\n{author.mention} **✗** {user.mention}"
            moji = "٩(ఠ益ఠ)۶"
        elif emotion_type == "sad":
            description = f"**{emotion_name}**\n{author.mention} **◊** {user.mention}"
            moji = random.choice(["( ╥ω╥ )", "	(ಡ‸ಡ)"])
        elif emotion_type == "blush":
            description = f"**{emotion_name}**\n{author.mention} **✧** {user.mention}"
            moji = random.choice(
                ["(⁄ ⁄•⁄ω⁄•⁄ ⁄)	", "(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)", "(„ಡωಡ„)	", "(//ω//)	"]
            )
        elif emotion_type == "friends":
            description = f"**{emotion_name}**\n{author.mention} **+** {user.mention}"
            moji = "(*＾ω＾)人(＾ω＾*)"
        else:
            description = f"**{emotion_name}\n{author.mention} **✧** {user.mention}"
            moji = "(ᴖ◡ᴖ)♪"
        if author_msg is not None:
            description = description + f"\n{author_msg}"
    else:
        description = f"**{emotion_name}**"
        if emotion_type == "positive":
            moji = "(ᴖ◡ᴖ)♪"
        elif emotion_type == "neutral":
            moji = random.choice(
                ["┐(￣ヮ￣)┌", "(•ิ_•ิ)?", "	ლ(ಠ_ಠ ლ)", "	(・_・ヾ", "(↼_↼)"]
            )
        elif emotion_type == "angry":
            moji = "٩(ఠ益ఠ)۶"
        elif emotion_type == "sad":
            moji = random.choice(["( ╥ω╥ )", "	(ಡ‸ಡ)"])
        elif emotion_type == "blush":
            moji = random.choice(
                ["(⁄ ⁄•⁄ω⁄•⁄ ⁄)	", "(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)", "(„ಡωಡ„)	", "(//ω//)	"]
            )
        elif emotion_type == "friends":
            moji = "(*＾ω＾)人(＾ω＾*)"
        else:
            moji = "(ᴖ◡ᴖ)♪"
        if author_msg is not None:
            description = description + f"\n{author_msg}"
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, description=description)
    embed.set_image(url=random.choice(gifs))
    if is_free is True:
        footer = f"{moji}"
    else:
        msg = get_msg_from_locale_by_key(guild_id, "you_charged")
        bal_msg = get_msg_from_locale_by_key(guild_id, "on_balance")
        balance = get_user_balance(guild_id, author.id)
        footer = f"{moji}\n{msg} -{cost}\n{bal_msg} {balance}"
    embed.set_footer(text=footer, icon_url=author.display_avatar)
    return embed


def create_emotions_cost_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS emotions_cost (guild_id INTEGER, emotions_for_money_state BOOL, cost INTEGER) """
    )
    db.commit()
    cursor.close()
    db.close()
    return
