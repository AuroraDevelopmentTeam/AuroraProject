import sqlite3
import asyncio

import nextcord

from core.embeds import DEFAULT_BOT_COLOR
from core.emojify import TEAM, LOCK, UNLOCK, PEN, KICK, YES, NO, CROWN, MUTE, MICROPHONE


class VoiceRoomName(nextcord.ui.Modal):
    def __init__(self, title: str, voice_room: nextcord.VoiceChannel):
        self.voice_room = voice_room
        super().__init__(title)
        self.embedName = nextcord.ui.TextInput(
            label="Voice Room Name",
            min_length=1,
            max_length=100,
            required=True,
            placeholder="Cool name",
        )
        self.add_item(self.embedName)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            name = self.embedName.value
            voice_room = self.voice_room
            await voice_room.edit(name=name)
            await interaction.response.send_message(embed=nextcord.Embed(
                description=f"{YES}",
                colour=DEFAULT_BOT_COLOR), ephemeral=True)
        except:
            await interaction.response.send_message(embed=nextcord.Embed(
                description=f"{NO}",
                colour=DEFAULT_BOT_COLOR), ephemeral=True)


class VoiceRoomLimit(nextcord.ui.Modal):
    def __init__(self, title: str, voice_room: nextcord.VoiceChannel):
        self.voice_room = voice_room
        super().__init__(title)
        self.embedName = nextcord.ui.TextInput(
            label="Voice Room Limit",
            min_length=1,
            max_length=2,
            required=True,
            placeholder="1-99",
        )
        self.add_item(self.embedName)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            name = self.embedName.value
            voice_room = self.voice_room
            if name.isdigit():
                user_limit = int(name)
                await voice_room.edit(user_limit=int(user_limit))
                await interaction.response.send_message(embed=nextcord.Embed(
                    description=f"{YES}",
                    colour=DEFAULT_BOT_COLOR), ephemeral=True)
            else:
                await interaction.response.send_message(embed=nextcord.Embed(
                    description=f"{NO}",
                    colour=DEFAULT_BOT_COLOR), ephemeral=True)
        except:
            pass


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
        description=f"""
        {PEN} - **изменить** название комнаты\n
        {TEAM} - **изменить** кол-во слотов\n
        {LOCK} - **закрыть** комнату для всех\n
        {UNLOCK} - **открыть** комнату для всех\n
        {KICK} - **выгнать** пользователя с комнаты\n
        {YES} - **дать доступ пользователю** в комнату\n
        {NO} - **забрать доступ пользователю** в комнату\n
        {MICROPHONE} - **размутить** пользователя\n
        {MUTE} - **замутить** пользователя\n
        {CROWN} - **передать владение** комнатой
    """,
        colour=DEFAULT_BOT_COLOR
    )
    return embed


def create_button_reaction_embed(custom_id: str) -> nextcord.Embed:
    if custom_id == "private_room:name":
        embed = nextcord.Embed(
            title="Изменение имени комнаты",
            description="Напишите сообщением ниже новое название для комнаты, у вас есть 30 секунд на выполнение "
                        "операции.",
            colour=DEFAULT_BOT_COLOR
        )
    elif custom_id == 'private_room:users':
        embed = nextcord.Embed(
            title="Изменение лимита пользователей",
            description="Напишите сообщением ниже лимит пользователей комнаты в виде цифры"
                        ", у вас есть 30 секунд на выполнение операции.",
            colour=DEFAULT_BOT_COLOR
        )
    elif custom_id == 'private_room:kick':
        embed = nextcord.Embed(
            title="Кик пользователей с комната",
            description="Напишите сообщением ниже упоминание **@Пользователя**, "
                        "находящегося с вами в комнате, которого вы хотите кикнуть",
            colour=DEFAULT_BOT_COLOR
        )
    elif custom_id == 'private_room:add':
        embed = nextcord.Embed(
            title="Добавить пользователя в комнату",
            description="Напишите сообщением ниже упоминание **@Пользователя**, "
                        "чтобы разрешить ему заходить в вашу комнату",
            colour=DEFAULT_BOT_COLOR
        )
    elif custom_id == 'private_room:remove':
        embed = nextcord.Embed(
            title="Запретить пользователю вход в комнату",
            description="Напишите сообщением ниже упоминание **@Пользователя**, "
                        "чтобы запретить ему заходить в вашу комнату",
            colour=DEFAULT_BOT_COLOR
        )
    elif custom_id == 'private_room:unmute':
        embed = nextcord.Embed(
            title="Разрешить пользователю говорить",
            description="Напишите сообщением ниже упоминание **@Пользователя**, "
                        "чтобы разрешить ему говорить в вашей комнате",
            colour=DEFAULT_BOT_COLOR
        )
    elif custom_id == 'private_room:mute':
        embed = nextcord.Embed(
            title="Запретить пользователю говорить",
            description="Напишите сообщением ниже упоминание **@Пользователя**, "
                        "чтобы запретить ему говорить в вашей комнате",
            colour=DEFAULT_BOT_COLOR
        )
    elif custom_id == 'private_room:leadership':
        embed = nextcord.Embed(
            title="Передать пользователю управление комнатой",
            description="Напишите сообщением ниже упоминание **@Пользователя**, "
                        "чтобы передать ему управление комнатой",
            colour=DEFAULT_BOT_COLOR
        )
    else:
        embed = nextcord.Embed(
            title="0",
            description="error, no custom_id",
            colour=DEFAULT_BOT_COLOR
        )
    return embed


async def react_on_private_room_menu_button(client, interaction: nextcord.Interaction,
                                            custom_id: str, voice_room: nextcord.VoiceChannel, voices: dict):
    if custom_id == "private_room:name":
        modal = VoiceRoomName("name", voice_room)
        return await interaction.response.send_modal(modal)
    elif custom_id == 'private_room:users':
        modal = VoiceRoomLimit("limit", voice_room)
        return await interaction.response.send_modal(modal)
    elif custom_id == 'private_room:lock':
        await interaction.response.defer()
        try:
            await voice_room.set_permissions(
                interaction.guild.default_role,
                connect=False
            )
            await interaction.followup.send(embed=nextcord.Embed(
                description=f"{LOCK}\n{YES}",
                colour=DEFAULT_BOT_COLOR), ephemeral=True)
        except:
            await interaction.followup.send(embed=nextcord.Embed(
                description=f"{LOCK}\n{NO}",
                colour=DEFAULT_BOT_COLOR), ephemeral=True)
    elif custom_id == 'private_room:unlock':
        await interaction.response.defer()
        try:
            await voice_room.set_permissions(
                interaction.guild.default_role,
                connect=True
            )
            await interaction.followup.send(embed=nextcord.Embed(
                description=f"{UNLOCK}\n{YES}",
                colour=DEFAULT_BOT_COLOR), ephemeral=True)
        except:
            await interaction.followup.send(embed=nextcord.Embed(
                description=f"{UNLOCK}\n{NO}",
                colour=DEFAULT_BOT_COLOR), ephemeral=True)
    elif custom_id == 'private_room:kick':
        await interaction.response.defer()
        await interaction.followup.send(embed=create_button_reaction_embed(custom_id), ephemeral=True)
        msg = await client.wait_for("message", check=lambda message: message.author == interaction.user, timeout=30)
        try:
            if len(msg.mentions):
                for user in msg.mentions:
                    if user.voice.channel == voice_room:
                        await user.move_to(channel=None)
            await msg.add_reaction(YES)
        except:
            await msg.add_reaction(NO)
        await msg.delete(delay=5)
    elif custom_id == 'private_room:add':
        await interaction.response.defer()
        await interaction.followup.send(embed=create_button_reaction_embed(custom_id), ephemeral=True)
        msg = await client.wait_for("message", check=lambda message: message.author == interaction.user, timeout=30)
        try:
            if len(msg.mentions):
                for user in msg.mentions:
                    await voice_room.set_permissions(
                        user,
                        connect=True
                    )
            await msg.add_reaction(YES)
        except:
            await msg.add_reaction(NO)
        await msg.delete(delay=5)
    elif custom_id == 'private_room:remove':
        await interaction.response.defer()
        await interaction.followup.send(embed=create_button_reaction_embed(custom_id), ephemeral=True)
        msg = await client.wait_for("message", check=lambda message: message.author == interaction.user, timeout=30)
        try:
            if len(msg.mentions):
                for user in msg.mentions:
                    await voice_room.set_permissions(
                        user,
                        connect=False
                    )
            await msg.add_reaction(YES)
        except:
            await msg.add_reaction(NO)
        await msg.delete(delay=5)
    elif custom_id == 'private_room:unmute':
        await interaction.response.defer()
        await interaction.followup.send(embed=create_button_reaction_embed(custom_id), ephemeral=True)
        msg = await client.wait_for("message", check=lambda message: message.author == interaction.user, timeout=30)
        try:
            if len(msg.mentions):
                for user in msg.mentions:
                    await voice_room.set_permissions(
                        user,
                        speak=True
                    )
            await msg.add_reaction(YES)
        except:
            await msg.add_reaction(NO)
        await msg.delete(delay=5)
    elif custom_id == 'private_room:mute':
        await interaction.response.defer()
        await interaction.followup.send(embed=create_button_reaction_embed(custom_id), ephemeral=True)
        msg = await client.wait_for("message", check=lambda message: message.author == interaction.user, timeout=30)
        try:
            if len(msg.mentions):
                for user in msg.mentions:
                    await voice_room.set_permissions(
                        user,
                        speak=False
                    )
            await msg.add_reaction(YES)
        except:
            await msg.add_reaction(NO)
        await msg.delete(delay=5)
    elif custom_id == 'private_room:leadership':
        await interaction.response.defer()
        await interaction.followup.send(embed=create_button_reaction_embed(custom_id), ephemeral=True)
        msg = await client.wait_for("message", check=lambda message: message.author == interaction.user, timeout=15)
        try:
            if len(msg.mentions):
                voices[voice_room.id] = msg.mentions[0].id
                await voice_room.set_permissions(
                    msg.mentions[0],
                    connect=True, speak=True, deafen_members=True, priority_speaker=True,
                    view_channel=True, manage_channels=True, mute_members=True, move_members=True, stream=True,
                )
                await voice_room.set_permissions(
                    interaction.user,
                    connect=True, speak=True, deafen_members=False, priority_speaker=False,
                    view_channel=True, manage_channels=False, mute_members=False, move_members=False, stream=True,
                )
                await msg.add_reaction(YES)
        except:
            await msg.add_reaction(NO)
        await msg.delete(delay=5)
    else:
        pass
