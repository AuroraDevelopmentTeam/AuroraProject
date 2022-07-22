import random

import nextcord

from core.locales.getters import get_msg_from_locale_by_key
from core.embeds import DEFAULT_BOT_COLOR


def create_emotion_embed(guild_id: int, emotion_name: str, emotion_type: str, author: nextcord.Member,
                         gifs: list, user: nextcord.Member = None,
                         author_msg: str = None) -> nextcord.Embed:
    emotion_name = get_msg_from_locale_by_key(guild_id, f'emotion_{emotion_name}')
    if user is not None:
        if emotion_type == 'positive':
            description = f'**{emotion_name}**\n{author.mention} **✧** {user.mention}'
            moji = '(ᴖ◡ᴖ)♪'
        elif emotion_type == 'neutral':
            description = f'**{emotion_name}**\n{author.mention} **○** {user.mention}'
            moji = random.choice(['┐(￣ヮ￣)┌', '(•ิ_•ิ)?', '	ლ(ಠ_ಠ ლ)', "	(・_・ヾ", "(↼_↼)"])
        elif emotion_type == 'angry':
            description = f'**{emotion_name}**\n{author.mention} **✗** {user.mention}'
            moji = '٩(ఠ益ఠ)۶'
        elif emotion_type == 'sad':
            description = f'**{emotion_name}**\n{author.mention} **◊** {user.mention}'
            moji = random.choice(["( ╥ω╥ )", "	(ಡ‸ಡ)"])
        elif emotion_type == 'blush':
            description = f'**{emotion_name}**\n{author.mention} **✧** {user.mention}'
            moji = random.choice(['(⁄ ⁄•⁄ω⁄•⁄ ⁄)	', '(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)', '(„ಡωಡ„)	', '(//ω//)	'])
        elif emotion_type == 'friends':
            description = f'**{emotion_name}**\n{author.mention} **+** {user.mention}'
            moji = '(*＾ω＾)人(＾ω＾*)'
        else:
            description = f'**{emotion_name}\n{author.mention} **✧** {user.mention}'
            moji = '(ᴖ◡ᴖ)♪'
        if author_msg is not None:
            description = description + f'\n{author_msg}'
    else:
        description = f'**{emotion_name}**'
        if emotion_type == 'positive':
            moji = '(ᴖ◡ᴖ)♪'
        elif emotion_type == 'neutral':
            moji = random.choice(['┐(￣ヮ￣)┌', '(•ิ_•ิ)?', '	ლ(ಠ_ಠ ლ)', "	(・_・ヾ", "(↼_↼)"])
        elif emotion_type == 'angry':
            moji = '٩(ఠ益ఠ)۶'
        elif emotion_type == 'sad':
            moji = random.choice(["( ╥ω╥ )", "	(ಡ‸ಡ)"])
        elif emotion_type == 'blush':
            moji = random.choice(['(⁄ ⁄•⁄ω⁄•⁄ ⁄)	', '(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)', '(„ಡωಡ„)	', '(//ω//)	'])
        elif emotion_type == 'friends':
            moji = '(*＾ω＾)人(＾ω＾*)'
        else:
            moji = '(ᴖ◡ᴖ)♪'
        if author_msg is not None:
            description = description + f'\n{author_msg}'
    embed = nextcord.Embed(color=DEFAULT_BOT_COLOR, description=description)
    embed.set_image(url=random.choice(gifs))
    embed.set_footer(text=moji, icon_url=author.display_avatar)
    return embed
