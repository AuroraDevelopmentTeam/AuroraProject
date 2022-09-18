from typing import Optional

import nextcord
from nextcord import Interaction, SlashOption, VoiceChannel, Permissions
from nextcord.ext import commands
from nextcord.abc import GuildChannel

from core.voice.updaters import update_voice_creation_room
from core.voice.getters import get_voice_creation_room
from core.voice.create import create_button_menu_embed, react_on_private_room_menu_button
from core.emojify import TEAM, LOCK, UNLOCK, PEN, KICK, YES, NO, CROWN, MUTE, MICROPHONE


class VoiceMenuButtonsView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=0)

    @nextcord.ui.button(label="", emoji=PEN, custom_id="private_room:name")
    async def _name(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji=TEAM, custom_id="private_room:users")
    async def _users(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji=LOCK, custom_id="private_room:lock")
    async def _lock(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji=UNLOCK, custom_id="private_room:unlock")
    async def _unlock(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji=KICK, custom_id="private_room:kick")
    async def _kick(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji=YES, custom_id="private_room:add")
    async def _add(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji=NO, custom_id="private_room:remove")
    async def _remove(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji=MICROPHONE, custom_id="private_room:unmute")
    async def _unmute(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji=MUTE, custom_id="private_room:mute")
    async def _mute(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass

    @nextcord.ui.button(label="", emoji=CROWN, custom_id="private_room:leadership")
    async def _leadership(self, button: nextcord.ui.button, interaction: nextcord.MessageInteraction):
        pass


class UserVoiceHandler(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voice_rooms = {}

    @commands.Cog.listener()
    async def on_disconnect(self):
        for voice_client in self.client.voice_clients:
            if voice_client.channel.id in self.voice_rooms:
                await voice_client.channel.delete()
                del self.voice_rooms[voice_client.channel.id]

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            server_voice_creation_room = get_voice_creation_room(after.channel.guild.id)
        except AttributeError:
            server_voice_creation_room = get_voice_creation_room(before.channel.guild.id)
        if member.bot:
            return
        if server_voice_creation_room == 0:
            return
        if after.channel and after.channel.id == server_voice_creation_room:
            overwrites = {
                interaction.guild.default_role: nextcord.PermissionOverwrite(
                    connect=False,
                ),
                role: nextcord.PermissionOverwrite(connect=True, speak=True, view_channel=True),
                member: nextcord.PermissionOverwrite(
                    connect=True, speak=True, deafen_members=True, priority_speaker=True,
                    view_channel=True, manage_channels=True, mute_members=True, move_members=True, stream=True,
                )
            }
            channel = await member.guild.create_voice_channel(
                name=f"{member}",
                category=after.channel.category,
                overwrites=overwrites
            )
            await member.move_to(channel=channel)
            self.voice_rooms[channel.id] = member.id
        if before.channel and before.channel.id in self.voice_rooms and not len(before.channel.members):
            await before.channel.delete()
            del self.voice_rooms[before.channel.id]

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction):
        if not interaction.user.voice:
            return
        if interaction.user.voice.channel.id not in self.voice_rooms:
            return
        try:
            custom_id = interaction.data["custom_id"]
            await react_on_private_room_menu_button(self.client, interaction, custom_id, interaction.user.voice.channel)
        except KeyError:
            pass

    @nextcord.slash_command(name="voice_private_config", description="configuration of voice channels",
                            default_member_permissions=Permissions(administrator=True),
                            )
    async def __voice_private_config(self, interaction: Interaction):
        pass

    @__voice_private_config.subcommand(name="voice_creation_channel")
    async def __voice_creation_channel_set(self, interaction: Interaction,
                                           channel: Optional[GuildChannel] = SlashOption(required=True), ):
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
