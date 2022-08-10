import random
from typing import Optional
import datetime
from datetime import timedelta

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Permissions, SlashOption

from core.stats.updaters import (
    update_user_messages_counter,
    update_user_join_time,
    update_user_time_in_voice,
)
from core.stats.getters import (
    get_user_join_time,
    get_user_time_in_voice,
    get_user_messages_counter,
)
from core.utils import format_seconds_to_hhmmss
from core.locales.getters import get_msg_from_locale_by_key
from core.embeds import construct_basic_embed


class StatisticsCounter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if not message.author.bot:
            update_user_messages_counter(message.guild.id, message.author.id, 1)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        if before.channel is not None and after.channel is None:
            join_time = get_user_join_time(member.guild.id, member.id)
            if join_time != "0":
                voice_leave_time = datetime.datetime.now().time().strftime("%H:%M:%S")
                calculate_time = abs(
                    datetime.datetime.strptime(voice_leave_time, "%H:%M:%S")
                    - datetime.datetime.strptime(join_time, "%H:%M:%S")
                )
                second_in_voice = abs(calculate_time.total_seconds())
                update_user_join_time(member.guild.id, member.id, "0")
                update_user_time_in_voice(member.guild.id, member.id, second_in_voice)
        elif before.channel is None and after.channel is not None:
            join_time = datetime.datetime.now().time().strftime("%H:%M:%S")
            update_user_join_time(member.guild.id, member.id, join_time)
        else:
            pass

    @nextcord.slash_command(
        name="online",
        default_member_permissions=Permissions(send_messages=True),
        description="Show your or user voice online",
    )
    async def __online(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(
            required=False,
            description="The discord's user, tag someone with @",
            description_localizations={
                "ru": "Пользователь дискорда, укажите кого-то @"
            },
        ),
    ):
        if user is None:
            user = interaction.user
        if user.bot:
            return await interaction.response.send_message("bot_user_error")
        voice_time = get_user_time_in_voice(interaction.guild.id, user.id)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{user.mention} {message} **{format_seconds_to_hhmmss(voice_time)}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
            )
        )

    @nextcord.slash_command(
        name="messages_counter",
        default_member_permissions=Permissions(send_messages=True),
        description="Show your or user messages counter",
    )
    async def __messages_counter(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(
            required=False,
            description="The discord's user, tag someone with @",
            description_localizations={
                "ru": "Пользователь дискорда, укажите кого-то @"
            },
        ),
    ):
        if user is None:
            user = interaction.user
        if user.bot:
            return await interaction.response.send_message("bot_user_error")
        msg_count = get_user_messages_counter(interaction.guild.id, user.id)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{user.mention} {message} **{msg_count}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
            )
        )


def setup(client):
    client.add_cog(StatisticsCounter(client))
