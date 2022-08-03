import random
from typing import Optional
import datetime
from datetime import timedelta

import nextcord
from nextcord.ext import commands
from nextcord import Interaction

from core.stats.updaters import update_user_messages_counter, update_user_join_time, update_user_time_in_voice
from core.stats.getters import get_user_join_time


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
            if join_time != '0':
                voice_leave_time = datetime.datetime.now().time().strftime('%H:%M:%S')
                calculate_time = abs(
                    datetime.datetime.strptime(voice_leave_time, '%H:%M:%S') - datetime.datetime.strptime(
                        join_time, '%H:%M:%S'))
                second_in_voice = abs(calculate_time.total_seconds())
                update_user_join_time(member.guild.id, member.id, '0')
                update_user_time_in_voice(member.guild.id, member.id, second_in_voice)
        elif before.channel is None and after.channel is not None:
            join_time = datetime.datetime.now().time().strftime('%H:%M:%S')
            update_user_join_time(member.guild.id, member.id, join_time)
        else:
            pass


def setup(client):
    client.add_cog(StatisticsCounter(client))
