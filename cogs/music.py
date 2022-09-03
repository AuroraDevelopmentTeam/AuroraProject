from typing import Optional

import nextcord
import wavelink
from core.embeds import construct_basic_embed
from core.errors import construct_error_bot_user_embed
from core.locales.getters import (get_localized_description,
                                  get_localized_name,
                                  get_msg_from_locale_by_key)
from easy_pil import *
from nextcord import Interaction, Permissions, SlashOption
from nextcord.ext import commands
from config import settings
from core.ui.buttons import create_button, ViewAuthorCheck
from core.utils import format_seconds_to_hhmmss


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.loop.create_task(self.connect_nodes())
        self.queue = wavelink.Queue()

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.client.wait_until_ready()

        await wavelink.NodePool.create_node(
            bot=self.client, host=settings["lava_host"], port=settings["lava_port"], password=settings["lava_password"]
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        await player.play(self.queue.get())

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
        search: str = SlashOption(
            required=True,
            description="search query or youtube link",
            description_localizations={
                "ru": "Поисковой запрос или ссылка YouTube"
            },
        ),
         
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
        #tracklist = await wavelink.YouTubeTrack.search(query=search)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.is_playing():
            self.queue.put(track)
            embed = construct_basic_embed(
                interaction.application_command.name,
                "Added to queue ",#**" + vc.track.info.get('title') + "**\n in channal *" + interaction.user.voice.channel.name + "*",
                search,
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        else:
            await vc.play(track)
        
            embed = construct_basic_embed(
                interaction.application_command.name,
                "Playing **" + vc.track.info.get('title') + "**\n in channal *" + interaction.user.voice.channel.name + "*",
                search,
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        #track_names = ""
        #for index, track in enumerate(tracks):
        #    track_names += f"**{index+1})** `" + track.title + "`\n\n"
        #    if index == 4:
        #        break
        
        await interaction.followup.send(embed=embed)

    @__play_music.on_autocomplete("search")
    async def searchauto(self, interaction: Interaction, search: str):
        if not search:
            # По стандарту выводим треки по запросу music
            tracks = await wavelink.YouTubeTrack.search(query="music", return_first=False)
            auto = []
            for track in tracks:
                auto.append(track.title + " (" + format_seconds_to_hhmmss(track.duration) + ")")
            await interaction.response.send_autocomplete(auto)
            return
        # Выводим треки по запросу search
        tracks = await wavelink.YouTubeTrack.search(query=search, return_first=False)
        auto = []
        for track in tracks:
            auto.append(track.title + " (" + format_seconds_to_hhmmss(track.duration) + ")")
        await interaction.response.send_autocomplete(auto)

    @__music.subcommand(
        name="stop",
        name_localizations=get_localized_name("music_stop"),
        description_localizations=get_localized_description("music_stop"),
    )
    async def __stop_music(
        self,
        interaction: Interaction,
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
        #tracklist = await wavelink.YouTubeTrack.search(query=search)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        embed = construct_basic_embed(
            interaction.application_command.name,
            "Stopped **" + vc.track.info.get('title') + "**\n in channal *" + interaction.user.voice.channel.name + "*",
            vc.track.info.get('title'),
            interaction.user.display_avatar,
            interaction.guild.id,
        )

        await vc.stop()
        await vc.disconnect()
        
        
        await interaction.followup.send(embed=embed)

    @__music.subcommand(
        name="skip",
        name_localizations=get_localized_name("music_skip"),
        description_localizations=get_localized_description("music_skip"),
    )
    async def __skip_music(
        self,
        interaction: Interaction,
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
        #tracklist = await wavelink.YouTubeTrack.search(query=search)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        embed = construct_basic_embed(
            interaction.application_command.name,
            "Stopped **" + vc.track.info.get('title') + "**\n in channal *" + interaction.user.voice.channel.name + "*",
            vc.track.info.get('title'),
            interaction.user.display_avatar,
            interaction.guild.id,
        )

        await vc.stop()
        await vc.play(self.queue.get())
        
        
        await interaction.followup.send(embed=embed)

    

def setup(client):
    client.add_cog(Music(client))
