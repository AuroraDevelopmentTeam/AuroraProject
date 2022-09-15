from typing import Optional

import nextcord
from nextcord import Interaction, SlashOption, VoiceChannel
from nextcord.ext import commands
from nextcord.abc import GuildChannel

from core.voice.updaters import update_voice_creation_room
from core.voice.getters import get_voice_creation_room
from core.voice.create import create_button_menu_embed


class VoiceMenuButtonsView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=0)

    @nextcord.ui.button(label="", emoji="🖊️")
    async def _name(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji="👥")
    async def _users(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji="🔒")
    async def _lock(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji="🔓")
    async def _unlock(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji="🚪")
    async def _kick(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji="✔")
    async def _add(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji="❌")
    async def _remove(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji="🔉")
    async def _unmute(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji="🔇")
    async def _mute(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji="👑")
    async def _korona(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass


class UserVoiceHandler(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voice_rooms = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        server_voice_creation_room = get_voice_creation_room(after.channel.guild.id)
        if member.bot:
            return
        if server_voice_creation_room == 0:
            return
        if after.channel and after.channel.id == server_voice_creation_room:
            channel = await member.guild.create_voice_channel(
                name=f"{member}",
                category=after.channel.category
            )
            await member.move_to(channel=channel)
            self.voice_rooms[channel.id] = member.id
        if before.channel and before.channel.id in self.voice_rooms and not len(before.channel.members):
            await before.channel.delete()
            del self.voice_rooms[before.channel.id]

    @nextcord.slash_command(name="voice_private_config", description="configuration of voice channels")
    async def __voice_private_config(self, interaction: Interaction):
        pass

    @__voice_private_config.subcommand(name="voice_creation_channel")
    async def __voice_creation_channel_set(self, interaction: Interaction,
                                           channel: Optional[GuildChannel] = SlashOption(required=True)):
        if isinstance(channel, VoiceChannel):
            update_voice_creation_room(interaction.guild.id, channel.id)
            await interaction.response.send_message('done')
        else:
            pass

    @__voice_private_config.subcommand(name="menu_invoke", description="invoke button menu for voice rooms")
    async def ____voice_creation_channel_menu_invoke(self, interaction: Interaction):
        await interaction.response.send_message(embed=create_button_menu_embed(), view=VoiceMenuButtonsView())


def setup(client):
    client.add_cog(UserVoiceHandler(client))
