from typing import Optional

import nextcord
import wavelink
from core.embeds import construct_basic_embed
from core.errors import construct_error_bot_user_embed
from core.locales.getters import (
    get_localized_description,
    get_localized_name,
    get_msg_from_locale_by_key,
)
from easy_pil import *
from nextcord import Interaction, Permissions, SlashOption
from nextcord.ext import commands


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.client.wait_until_ready()

        await wavelink.NodePool.create_node(
            bot=self.client, host="127.0.0.1", port=2333, password="secretpassword"
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

    @nextcord.slash_command(
        name="music",
        description="music player controle",
        name_localizations=get_localized_name("music"),
        description_localizations=get_localized_description("music"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __music(
        self,
        interaction: Interaction,
    ):
        """
        This is the set slash command that will be the prefix of music commands.
        """
        pass

    @__music.subcommand(
        name="play",
        name_localizations=get_localized_name("music_play"),
        description_localizations=get_localized_description("music_play"),
    )
    async def __play_music(
        self,
        interaction: Interaction,
        search: Optional[str] = SlashOption(required=True),
    ):
        await interaction.response.defer()
        user = interaction.user

        if user.bot:
            return await interaction.followup.send(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        track = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.play(track)
        embed = construct_basic_embed(
            interaction.application_command.name,
            "searcing and playing " + search,
            search,
            interaction.user.display_avatar,
            interaction.guild.id,
        )
        await interaction.followup.send(embed=embed)


def setup(client):
    client.add_cog(Music(client))
