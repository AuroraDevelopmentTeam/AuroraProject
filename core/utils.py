from __future__ import annotations

import typing
from typing import Type, Any, List, Optional

from config import settings

import nextcord
from core.checkers import is_user_in_table
from core.db_utils import execute_update, fetch_one
from core.locales.getters import get_msg_from_locale_by_key

from nextcord import Interaction, SelectOption, ChannelType
from contextlib import suppress
from nextcord.ui import ChannelSelect, Modal, Select, view, select, View, channel_select

__all__ = ("ModalInput", "SelectPrompt", "ChannelSelectPrompt")


def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60 * 60)
    seconds %= 60 * 60
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)


async def write_member_in_money(guild: nextcord.Guild, member: nextcord.Member):
    guild_starting_balance = await fetch_one(
        f"SELECT guild_starting_balance FROM money_config WHERE guild_id = {guild.id}"
    )
    if not member.bot:
        if await is_user_in_table("money", guild.id, member.id) is False:
            sql = "INSERT INTO money(guild_id, user_id, balance) VALUES (%s, %s, %s)"
            val = (guild.id, member.id, guild_starting_balance[0])
            await execute_update(sql, val)


async def write_member_in_levels(guild: nextcord.Guild, member: nextcord.Member) -> None:
    if not member.bot:
        if await is_user_in_table("levels", guild.id, member.id) is False:
            sql = (
                "INSERT INTO levels(guild_id, user_id, level, exp) VALUES (%s, %s, %s, %s)"
            )
            val = (guild.id, member.id, 1, 0)
            await execute_update(sql, val)


async def write_member_in_marriage(guild: nextcord.Guild, member: nextcord.Member) -> None:
    if not member.bot:
        if await is_user_in_table("marriage", guild.id, member.id) is False:
            sql = (
                "INSERT INTO marriage(guild_id, user_id, pair_id, like_id, divorces, love_description, "
                "date, family_money) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )
            val = (guild.id, member.id, 0, 0, 0, "0", "0", 0)
            await execute_update(sql, val)


async def write_member_in_gifts(guild: nextcord.Guild, member: nextcord.Member) -> None:
    if not member.bot:
        if await is_user_in_table("gifts", guild.id, member.id) is False:
            sql = (
                "INSERT INTO gifts(guild_id, user_id, gift_1, gift_2, gift_3, gift_4, gift_5, gift_6, "
                "gift_7, gift_8, gift_9, gift_10, gift_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            val = (guild.id, member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            await execute_update(sql, val)


async def write_member_in_honor(member: nextcord.Member) -> None:
    if not member.bot:
        if (
                await fetch_one(
                    f"SELECT user_id FROM honor WHERE user_id = {member.id}"
                )
                is None
        ):
            sql = (
                "INSERT INTO honor(user_id, honor_level, honor_points) VALUES (%s, %s, %s)"
            )
            val = (member.id, 2, 0)
            await execute_update(sql, val)


async def write_member_in_profiles(guild: nextcord.Guild, member: nextcord.Member) -> None:
    description = get_msg_from_locale_by_key(guild.id, "default_profile_description")
    if not member.bot:
        if (
                await fetch_one(
                    f"SELECT user_id FROM profiles WHERE user_id = {member.id}"
                )
                is None
        ):
            sql = "INSERT INTO profiles(user_id, description, avatar_form) VALUES (%s, %s, %s)"
            val = (
                member.id,
                description,
                settings["default_profile_avatar_form"],
            )
            await execute_update(sql, val)


async def write_member_in_stats(guild: nextcord.Guild, member: nextcord.Member) -> None:
    if not member.bot:
        if await is_user_in_table("stats", guild.id, member.id) is False:
            sql = "INSERT INTO stats(guild_id, user_id, messages, in_voice, join_time) VALUES (%s, %s, %s, %s, %s)"
            val = (guild.id, member.id, 0, 0, "0")
            await execute_update(sql, val)


async def write_member_in_badges(guild: nextcord.Guild, member: nextcord.Member) -> None:
    if not member.bot:
        if await is_user_in_table("badges", guild.id, member.id) is False:
            sql = (
                "INSERT INTO badges(guild_id, user_id, badge_1, badge_2, badge_3, badge_4, badge_5, badge_6, "
                "badge_7, badge_8, badge_9) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            val = (
                guild.id,
                member.id,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            )
            await execute_update(sql, val)


async def write_member_in_clan(guild: nextcord.Guild, member: nextcord.Member) -> None:
    if not member.bot:
        if await is_user_in_table("clan_members", guild.id, member.id) is False:
            sql = "INSERT INTO clan_members(guild_id, user_id, clan_id, join_date) VALUES (%s, %s, %s, %s)"
            val = (guild.id, member.id, 0, "0")
            await execute_update(sql, val)


class PlatformType:
    def __init__(self):
        pass


class MobilePlatform(PlatformType):
    def __init__(self):
        super().__init__()


class DesktopPlatform(PlatformType):
    def __init__(self):
        super().__init__()


def parse_status_to_int(status: nextcord.Status) -> int:
    status_parse_to_int = {
        nextcord.Status.offline: 0,
        nextcord.Status.invisible: 0,
        nextcord.Status.dnd: 1,
        nextcord.Status.do_not_disturb: 1,
        nextcord.Status.idle: 2,
        nextcord.Status.online: 3,
    }
    return status_parse_to_int[status]


def calculate_platform_type(
        user: typing.Union[nextcord.User, nextcord.Member]
) -> Type[PlatformType]:
    desktop_status = parse_status_to_int(user.desktop_status)
    browser_status = parse_status_to_int(user.web_status)
    mobile_status = parse_status_to_int(user.mobile_status)
    if (
            mobile_status >= desktop_status
            or mobile_status >= browser_status + desktop_status
    ):
        return MobilePlatform
    else:
        return DesktopPlatform


class ModalInput(Modal):
    def __init__(
        self,
        *,
        title: str,
        timeout: Optional[float] = None,
        custom_id: str = "modal_input",
        ephemeral: bool = False,
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.ephemeral = ephemeral

    async def on_submit(self, interaction: Interaction) -> None:
        with suppress(Exception):
            await interaction.response.defer(ephemeral=self.ephemeral)


class SelectPrompt(View):
    """
    This class is a subclass of the `View` class that is intended to be used as a base class for creating a select prompt.

    Parameters:
        placeholder (str): The placeholder text that will be displayed in the select prompt.
        options (List[SelectOption]): A list of `SelectOption` instances that will be displayed as options in the select prompt.
        max_values (int, optional): The maximum number of options that can be selected by the user. Default is 1.
        ephemeral (bool, optional): A boolean indicating whether the select prompt will be sent as an ephemeral message or not. Default is False.
    """

    def __init__(
            self, placeholder: str, options: List[SelectOption], max_values: int = 1, ephemeral: bool = False
    ) -> None:
        super().__init__()
        self.children[0].placeholder, self.children[0].max_values, self.children[
            0].options = placeholder, max_values, options  # type: ignore
        self.values = None
        self.ephemeral = ephemeral

    @select()
    async def select_callback(self, interaction: Interaction, select: Select):
        await interaction.response.defer(ephemeral=self.ephemeral)
        if self.ephemeral:
            await interaction.delete_original_message()
        else:
            with suppress(Exception):
                await interaction.message.delete()  # type: ignore
        self.values = select.values
        self.stop()


class ChannelSelectPrompt(View):
    """
    This class is a subclass of the `View` class that is intended to be used as a base class for creating a channel select prompt.

    Parameters:
        placeholder (str): The placeholder text that will be displayed in the channel select prompt.
        ephemeral (bool, optional): A boolean indicating whether the select prompt will be sent as an ephemeral message or not. Default is False.
        max_values (int, optional): The maximum number of options that can be selected by the user. Default is 1.
    """

    def __init__(self, placeholder: str = "Select a channel...", ephemeral: bool = False, max_values: int = 1) -> None:
        super().__init__()
        self.values = None
        self.ephemeral = ephemeral

        # Создание ChannelSelect с параметрами
        channel_select = ChannelSelect(
            placeholder=placeholder,
            max_values=max_values,
            channel_types=[ChannelType.text, ChannelType.voice, ChannelType.category]
        )

        # Добавление ChannelSelect в View
        self.add_item(channel_select)

        # Связывание callback вручную
        channel_select.callback = self.channel_select_callback

    async def channel_select_callback(self, interaction: Interaction):
        select = interaction.data  # Извлечение данных из взаимодействия (Interaction)

        if self.ephemeral:
            # Использование interaction.response для удаления сообщения, если оно было отправлено как ephemeral
            await interaction.response.defer()  # Завершаем взаимодействие без отправки сообщения
        else:
            with suppress(Exception):
                await interaction.message.delete()  # Удаление исходного сообщения

        # Получение каналов из select и сохранение их в self.values
        selected_channel_ids = select.get('values', [])
        selected_channels = [interaction.guild.get_channel(int(channel_id)) for channel_id in selected_channel_ids]

        # Сохранение выбранных каналов
        self.values = selected_channels
        self.stop()
