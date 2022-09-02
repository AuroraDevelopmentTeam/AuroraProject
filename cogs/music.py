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
        search: Optional[str] = SlashOption(
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
        tracks = await wavelink.YouTubeTrack.search(query=search, return_first=False)
        #tracklist = await wavelink.YouTubeTrack.search(query=search)
        """
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
        """
        track_names = ""
        for index, track in enumerate(tracks):
            track_names += f"**{index+1})** `" + track.title + "`\n\n"
            if index == 4:
                break
        embed = nextcord.Embed(
                title="Select track",
                description=f"Выберете один из трэков\n\n "
                            f"{track_names}",
            )
        first_button = create_button(
                "1️⃣",
                False,
                False,
            )
        second_button = create_button(
                "2️⃣",
                False,
                False,
            )
        third_button = create_button(
                "3️⃣",
                False,
                False,
            )
        four_button = create_button(
                "4️⃣",
                False,
                False,
            )
        five_button = create_button(
                "5️⃣",
                False,
                False,
            )
        view = ViewAuthorCheck(interaction.user)
        view.add_item(first_button)
        view.add_item(second_button)
        view.add_item(third_button)
        view.add_item(four_button)
        view.add_item(five_button)
        await interaction.followup.send(embed=embed, view=view)

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
