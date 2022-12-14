import requests
import textwrap
from typing import Optional

import nextcord
import wavelink
from config import settings
from core.embeds import construct_basic_embed
from core.errors import (construct_error_bot_user_embed,
                         construct_error_no_voice_embed)
from core.locales.getters import (get_localized_description,
                                  get_localized_name,
                                  get_msg_from_locale_by_key)
from core.ui.buttons import ViewAuthorCheck, create_button
from core.utils import format_seconds_to_hhmmss
from easy_pil import *
from nextcord import Interaction, Permissions, SlashOption
from nextcord.ext import commands
from vk_api import VkApi
from vk_api import audio as vka
import base64 


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
                "ru": "?????????????????? ???????????? ?????? ???????????? YouTube, VK, Spotify"
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
        # tracklist = await wavelink.YouTubeTrack.search(query=search)
        if not interaction.guild.voice_client:
                
            try:
                vc: wavelink.Player = await interaction.user.voice.channel.connect(
                    cls=wavelink.Player
                )
            except:
                embed=construct_error_no_voice_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "user_not_in_voice"),
                    self.client.user.avatar.url,
                )
                await interaction.followup.send(embed=embed)
                return
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.is_playing():
            self.queue.put(track)
            title = track.title
            embed = construct_basic_embed(
                interaction.application_command.name,
                "{title} added to queue ",
                search,
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        else:
            await vc.play(track)
            title = vc.track.info.get('title')
            channal = interaction.user.voice.channel.name
            embed = construct_basic_embed(
                interaction.application_command.name,
                f"Playing **{title}**\n in channal *{channal}*",
                search,
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        # track_names = ""
        # for index, track in enumerate(tracks):
        #    track_names += f"**{index+1})** `" + track.title + "`\n\n"
        #    if index == 4:
        #        break

        await interaction.followup.send(embed=embed)

    @__play_music.on_autocomplete("search")
    async def searchauto(self, interaction: Interaction, search: str):
        if not search:
            # ???? ?????????????????? ?????????????? ?????????? ???? ?????????????? music
            tracks = await wavelink.YouTubeTrack.search(query="music", return_first=False)
            auto = []
            for track in tracks:
                title = textwrap.shorten(track.title, width=75, placeholder="...")
                duration = format_seconds_to_hhmmss(track.duration)
                if duration[:3] == "00:":
                    duration = duration[3:]
                auto.append(f"{title} ({duration})")
            await interaction.response.send_autocomplete(auto)
            return
        # ?????????????? ?????????? ???? ?????????????? search
        tracks = await wavelink.YouTubeTrack.search(query=search, return_first=False)
        auto = []
        for track in tracks:
            title = textwrap.shorten(track.title, width=75, placeholder="...")
            duration = format_seconds_to_hhmmss(track.duration)
            if duration[:3] == "00:":
                duration = duration[3:]
            auto.append(f"{title} ({duration})")
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
        # tracklist = await wavelink.YouTubeTrack.search(query=search)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        embed = construct_basic_embed(
            interaction.application_command.name,
            "Player stopped",
            vc.track.info.get('title'),
            interaction.user.display_avatar,
            interaction.guild.id,
        )

        await vc.stop()
        await vc.disconnect()

        await interaction.followup.send(embed=embed)


    @__music.subcommand(
        name="test",
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
        # tracklist = await wavelink.YouTubeTrack.search(query=search)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        vk = VkApi('+79967719224', '@744qwetA*Pm5@#Y')
        vk.auth()
        #playlist = VkAudio(vk).parse_songs_in_playlist("asd")
        #tracks = playlist.get_audios()
        #track = tracks[0]
        tracks = vka.VkAudio(vk).get(-2000891248,13891248,'6a3202aee89f3750a6')
        track = str(tracks[0]['url'])
        b = track.encode("UTF-8")
        e = base64.b64encode(b)
        s1 = e.decode("UTF-8")
        #requests.get("http://localhost:2333/loadtracks?identifier=" + track)
        vktrack = await wavelink.LocalTrack.search(track)
        await vc.play(vktrack)
        #pldata = playlist.get_data()
        embed = construct_basic_embed(
            interaction.application_command.name,
            f"Testing: {tracks[0]['title']}",
            vc.track.info.get('title'),
            interaction.user.display_avatar,
            interaction.guild.id,
        )


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
        # tracklist = await wavelink.YouTubeTrack.search(query=search)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        title = vc.track.info.get('title')
        embed = construct_basic_embed(
            interaction.application_command.name,
            "Skipped **{title}**",
            vc.track.info.get('title'),
            interaction.user.display_avatar,
            interaction.guild.id,
        )

        await vc.stop()
        await vc.play(self.queue.get())

        await interaction.followup.send(embed=embed)


def setup(client):
    client.add_cog(Music(client))
