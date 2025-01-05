from typing import Optional

import nextcord
from nextcord import Interaction, Permissions, SlashOption
from nextcord.ext import commands, application_checks

from core.locales.getters import (
    get_localized_description,
    get_localized_name,
    get_msg_from_locale_by_key,
)
from core.emotions.create import create_emotion_embed
from core.emotions.storage import (
    kiss_gifs,
    hug_gifs,
    idk_gifs,
    respect_gifs,
    punch_gifs,
    cry_gifs,
    bite_gifs,
    spank_gifs,
    five_gifs,
    pat_gifs,
    lick_gifs,
    good_morning_gifs,
    good_night_gifs,
    run_gifs,
)
from core.emotions.getters import is_emotion_free, get_emotions_cost
from core.emotions.update import update_emotions_cost, update_emotions_for_money_state
from core.emotions.writers import write_in_emotions_cost_standart_values
from core.errors import (
    construct_error_self_choose_embed,
    construct_error_not_enough_embed,
    construct_error_negative_value_embed
)
from core.embeds import construct_basic_embed
from core.money.updaters import update_user_balance
from core.money.getters import get_user_balance, get_guild_currency_symbol


class Emotions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="emotion_config",
        description="Emotions slash command prefix",
        name_localizations=get_localized_name("emotion_config"),
        description_localizations=get_localized_description("emotion_config"),
        default_member_permissions=Permissions(administrator=True),
    )
    async def __emotion_config(self, interaction: Interaction):
        """
        This is the emotion_config slash command that will be the prefix of all emotions commands below.
        """
        pass

    @__emotion_config.subcommand(name="set_emotion_cost",
                                 description="Set cost of using emotion",
                                 name_localizations=get_localized_name("emotion_config_set_emotion_cost"),
                                 description_localizations=get_localized_description("emotion_config_set_emotion_cost"),
                                 )
    async def __emotion_config_set_emotion_cost(self, interaction: Interaction,
                                                money: Optional[int] = SlashOption(required=True)):
        if money < 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )
        await update_emotions_cost(interaction.guild.id, money)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"emotion_config_{interaction.application_command.name}"
        )
        currency_symbol = await get_guild_currency_symbol(interaction.guild.id)
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"emotion_config_{interaction.application_command.name}",
                f"{message} **{money}** {currency_symbol}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__emotion_config.subcommand(name="enable_paid_emotions",
                                 description="Turn on/Turn off currency paid emotions",
                                 name_localizations=get_localized_name("emotion_config_enable_paid_emotions"),
                                 description_localizations=get_localized_description("emotion_config_enable_paid_emotions"),
                                 )
    async def __emotion_config_enable_paid_emotions(self, interaction: Interaction,
                                                    enabled: Optional[bool] = SlashOption(required=True)):
        await update_emotions_for_money_state(interaction.guild.id, enabled)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"emotion_config_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if enabled is True:
            enabled = get_msg_from_locale_by_key(
                interaction.guild.id, "enabled"
            )
        else:
            enabled = get_msg_from_locale_by_key(
                interaction.guild.id, "disabled"
            )
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"emotion_config_{interaction.application_command.name}",
                f"{message} **{enabled}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="emotion",
        description="Emotions slash command prefix",
        name_localizations=get_localized_name("emotion"),
        description_localizations=get_localized_description("emotion"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __emotion(self, interaction: Interaction):
        """
        This is the emotion slash command that will be the prefix of all emotions commands below.
        """
        pass

    @__emotion.subcommand(
        name="kiss",
        description="Emotion command, send kissing emotion mentioning @User",
        name_localizations=get_localized_name("emotion_kiss"),
        description_localizations=get_localized_description("emotion_kiss"),
    )
    async def __kiss(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        if user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "positive",
            interaction.user,
            kiss_gifs,
            is_free,
            emotions_cost,
            user,
            message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="hug",
        description="Emotion command, send hugging emotion mentioning @User",
        name_localizations=get_localized_name("emotion_hug"),
        description_localizations=get_localized_description("emotion_hug"),
    )
    async def __hug(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        if user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "positive",
            interaction.user,
            hug_gifs,
            is_free,
            emotions_cost,
            user,
            message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="idk",
        description="Emotion command, send i dont know emotion for author",
        name_localizations=get_localized_name("emotion_idk"),
        description_localizations=get_localized_description("emotion_idk"),
    )
    async def __idk(
            self,
            interaction: Interaction,
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "neutral",
            interaction.user,
            idk_gifs,
            is_free,
            emotions_cost,
            author_msg=message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="f",
        description="PRESS F TO PAY RESPECTS",
        name_localizations=get_localized_name("emotion_f"),
        description_localizations=get_localized_description("emotion_f"),
    )
    async def __pay_respects(
            self,
            interaction: Interaction,
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "neutral",
            interaction.user,
            respect_gifs,
            is_free,
            emotions_cost,
            author_msg=message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="punch",
        description="Emotion command, send punching emotion mentioning @User",
        name_localizations=get_localized_name("emotion_punch"),
        description_localizations=get_localized_description("emotion_punch"),
    )
    async def __punch(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        if user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "angry",
            interaction.user,
            punch_gifs,
            is_free,
            emotions_cost,
            user,
            message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="cry",
        description="Emotion command, send crying emotion for author",
        name_localizations=get_localized_name("emotion_cry"),
        description_localizations=get_localized_description("emotion_cry"),
    )
    async def __cry(
            self,
            interaction: Interaction,
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "sad",
            interaction.user,
            cry_gifs,
            is_free,
            emotions_cost,
            author_msg=message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="bite",
        description="Emotion command, send bite emotion mentioning @User",
        name_localizations=get_localized_name("emotion_bite"),
        description_localizations=get_localized_description("emotion_bite"),
    )
    async def __bite(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        if user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "blush",
            interaction.user,
            bite_gifs,
            is_free,
            emotions_cost,
            user,
            message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="spank",
        description="Emotion command, send spank emotion mentioning @User",
        name_localizations=get_localized_name("emotion_spank"),
        description_localizations=get_localized_description("emotion_spank"),
    )
    async def __spank(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        if user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "blush",
            interaction.user,
            spank_gifs,
            is_free,
            emotions_cost,
            user,
            message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="highfive",
        description="Emotion command, send highfive emotion mentioning @User",
        name_localizations=get_localized_name("emotion_highfive"),
        description_localizations=get_localized_description("emotion_highfive"),
    )
    async def __highfive(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        if user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "friends",
            interaction.user,
            five_gifs,
            is_free,
            emotions_cost,
            user,
            message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="pat",
        description="Emotion command, send patting emotion mentioning @User",
        name_localizations=get_localized_name("emotion_pat"),
        description_localizations=get_localized_description("emotion_pat"),
    )
    async def __pat(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        if user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "positive",
            interaction.user,
            pat_gifs,
            is_free,
            emotions_cost,
            user,
            message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="lick",
        description="Emotion command, send lick emotion mentioning @User",
        name_localizations=get_localized_name("emotion_lick"),
        description_localizations=get_localized_description("emotion_lick"),
    )
    async def __lick(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        if user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "blush",
            interaction.user,
            lick_gifs,
            is_free,
            emotions_cost,
            user,
            message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="run",
        description="Emotion command, sends running emotion for author",
        name_localizations=get_localized_name("emotion_run"),
        description_localizations=get_localized_description("emotion_run"),
    )
    async def __run(
            self,
            interaction: Interaction,
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "neutral",
            interaction.user,
            run_gifs,
            is_free,
            emotions_cost,
            author_msg=message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="good_morning",
        description="Emotion command, sends running emotion for author",
        name_localizations=get_localized_name("emotion_good_morning"),
        description_localizations=get_localized_description("emotion_good_morning"),
    )
    async def __good_morning(
            self,
            interaction: Interaction,
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "positive",
            interaction.user,
            good_morning_gifs,
            is_free,
            emotions_cost,
            author_msg=message,
        )
        await interaction.response.send_message(embed=embed)

    @__emotion.subcommand(
        name="good_night",
        description="Emotion command, sends running emotion for author",
        name_localizations=get_localized_name("emotion_good_night"),
        description_localizations=get_localized_description("emotion_good_night"),
    )
    async def __good_night(
            self,
            interaction: Interaction,
            message: Optional[str] = SlashOption(
                required=False,
                description="Message pinned to emotion message",
                description_localizations={
                    "ru": "Сообщение, которое будет прикреплено к эмоции"
                },
            ),
    ):
        try:
            is_free = await is_emotion_free(interaction.guild.id)
            emotions_cost = await get_emotions_cost(interaction.guild.id)
        except TypeError:
            guilds = [interaction.guild]
            await write_in_emotions_cost_standart_values(guilds)
            return await interaction.response.send_message('Попробуйте ещё раз')
        if await is_emotion_free(interaction.guild.id) is False:
            emotions_cost = await get_emotions_cost(interaction.guild.id)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < emotions_cost:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                return await interaction.response.send_message(
                    embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    )
                )
            else:
                await update_user_balance(interaction.guild.id, interaction.user.id, -emotions_cost)
        embed = await create_emotion_embed(
            interaction.guild.id,
            interaction.application_command.name,
            "blush",
            interaction.user,
            good_night_gifs,
            is_free,
            emotions_cost,
            author_msg=message,
        )
        await interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(Emotions(client))
