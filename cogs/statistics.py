import random
from typing import Optional
import datetime
from datetime import timedelta

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Permissions, SlashOption
from nextcord.abc import GuildChannel

from core.stats.updaters import (
    update_user_messages_counter,
    update_user_join_time,
    update_user_time_in_voice,
)
from core.stats.getters import (
    get_user_join_time,
    get_user_time_in_voice,
    get_user_messages_counter,
    get_channel_stats_state,
)
from core.stats.writers import write_channel_in_config
from core.money.getters import (
    get_voice_minutes_for_income,
    get_guild_min_max_voice_income,
    get_guild_min_max_msg_income,
    get_msg_cooldown,
    get_channel_income_state,
)
from core.money.updaters import update_user_balance
from core.utils import format_seconds_to_hhmmss
from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_localized_description,
    get_localized_name,
)
from core.embeds import construct_basic_embed
from core.levels.getters import get_user_level, get_min_max_exp, get_user_exp
from core.levels.updaters import update_user_level, update_user_exp
from core.auto.roles.getters import check_level_autorole, get_server_level_autorole, get_autorole_lvl_deletion_state, \
    get_lesser_lvl_roles_list


class StatisticsCounter(commands.Cog):
    def __init__(self, client):
        self.client = client

    def level_up(self, guild_id, user_id):
        user_exp = get_user_exp(guild_id, user_id)
        user_level = get_user_level(guild_id, user_id)
        leveling_formula = round((7 * (user_level**2)) + 58)
        if user_exp >= leveling_formula:
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if not message.author.bot:
            try:
                if await get_channel_stats_state(message.guild.id, message.channel.id) is True:
                    await update_user_messages_counter(message.guild.id, message.author.id, 1)
                if await get_channel_income_state(message.guild.id, message.channel.id) is False:
                    return
                message_counter = await get_user_messages_counter(
                    message.guild.id, message.author.id
                )
                try:
                    messages_for_money = await get_msg_cooldown(message.guild.id)
                except TypeError as error:
                    messages_for_money = 10
                    print(error)
                if message_counter % messages_for_money == 0:
                    try:
                        min, max = await get_guild_min_max_msg_income(message.guild.id)
                        await update_user_balance(
                            message.guild.id, message.author.id, random.randint(min, max)
                        )
                    except TypeError:
                        pass
            except TypeError:
                pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        if before.channel is not None and after.channel is None:
            join_time = await get_user_join_time(member.guild.id, member.id)
            join_time = int(join_time)
            if join_time != 0:
                voice_leave_time = int(datetime.datetime.now().timestamp())
                calculate_time = voice_leave_time-join_time
                second_in_voice = calculate_time
                await update_user_join_time(member.guild.id, member.id, "0")
                await update_user_time_in_voice(member.guild.id, member.id, second_in_voice)

                minutes_in_voice = int(second_in_voice / 60)
                try:
                    voice_minutes_for_income = await get_voice_minutes_for_income(member.guild.id)
                    min, max = await get_guild_min_max_voice_income(member.guild.id)
                    money_to_update = (
                        int(minutes_in_voice // voice_minutes_for_income)
                    ) * random.randint(min, max)
                    await update_user_balance(member.guild.id, member.id, money_to_update)

                    min_exp, max_exp = await get_min_max_exp(member.guild.id)
                    exp = random.randint(min_exp, max_exp) * (int(minutes_in_voice // 5))
                    await update_user_exp(member.guild.id, member.id, exp, exp)
                    user_level = get_user_level(member.guild.id, member.id)
                    user_exp = get_user_exp(member.guild.id, member.id)
                    if user_exp > 0:
                        leveling_formula = round((7 * (user_level**2)) + 58)
                        while self.level_up(member.guild.id, member.id):
                            await update_user_exp(
                                member.guild.id,
                                member.id,
                                -leveling_formula,
                                -leveling_formula,
                            )
                            await update_user_level(member.guild.id, member.id, 1)
                            user_level = await get_user_level(member.guild.id, member.id)
                            if await check_level_autorole(member.guild.id, user_level) is True:
                                role = await get_server_level_autorole(
                                    member.guild.id, user_level
                                )
                                role = nextcord.utils.get(member.guild.roles, id=role)
                                await member.add_roles(role)
                                if await get_autorole_lvl_deletion_state(member.guild.id) is True:
                                    roles_list = await get_lesser_lvl_roles_list(member.guild.id, user_level)
                                    for rolee in roles_list:
                                        try:
                                            role = nextcord.utils.get(member.guild.roles, id=rolee[0])
                                            await member.remove_roles(role)
                                        except:
                                            pass
                            leveling_formula = round((7 * (user_level**2)) + 58)
                except TypeError:
                    return

        elif before.channel is None and after.channel is not None:
            join_time = str(int(datetime.datetime.now().timestamp()))
            await update_user_join_time(member.guild.id, member.id, join_time)
        else:
            pass

    @nextcord.slash_command(
        name="online",
        default_member_permissions=Permissions(send_messages=True),
        name_localizations=get_localized_name("online"),
        description_localizations=get_localized_description("online"),
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
        voice_time = await get_user_time_in_voice(interaction.guild.id, user.id)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}"
        )
        voice_members = set()
        for voice_channel in interaction.guild.voice_channels:
            for member in voice_channel.members:
                voice_members.add(member.id)
        message_2 = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}_peoples"
        )
        guild = await self.client.fetch_guild(interaction.guild.id)
        number_of_people_in_voice = len(voice_members)
        number_of_people_on_server = guild.approximate_member_count
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{user.mention} {message} **{format_seconds_to_hhmmss(voice_time)}**\n"
                f"{message_2} **{number_of_people_in_voice}/{number_of_people_on_server}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(name="messages_counter_channel",
                            name_localizations=get_localized_name("messages_counter_channel"),
                            description_localizations=get_localized_description("messages_counter_channel"),
                            )
    async def __messages_counter_channel(self, interaction: Interaction,
                                         channel: Optional[GuildChannel] = SlashOption(required=True),
                                         enabled: Optional[bool] = SlashOption(required=True)):
        await write_channel_in_config(interaction.guild.id, channel.id, enabled)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}"
        )
        message_2 = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}_2"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if enabled is True:
            enabled = get_msg_from_locale_by_key(interaction.guild.id, "enabled")
        else:
            enabled = get_msg_from_locale_by_key(interaction.guild.id, "disabled")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} {channel.mention} {message_2} **{enabled}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="messages_counter",
        default_member_permissions=Permissions(send_messages=True),
        name_localizations=get_localized_name("messages_counter"),
        description_localizations=get_localized_description("messages_counter"),
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
        msg_count = await get_user_messages_counter(interaction.guild.id, user.id)
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
                interaction.guild.id,
            )
        )


def setup(client):
    client.add_cog(StatisticsCounter(client))
