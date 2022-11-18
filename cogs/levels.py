import asyncio
from typing import Optional
from easy_pil import *
from PIL import Image
from io import BytesIO

import cooldowns
import nextcord
from nextcord.abc import GuildChannel
from nextcord.ext import commands, application_checks
from nextcord import Interaction, SlashOption, Permissions

from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_localized_description,
    get_localized_name,
)
from core.levels.getters import (
    get_user_exp,
    get_user_level,
    get_min_max_exp,
    get_guild_messages_state,
    get_channel_level_state
)
from core.levels.updaters import (
    update_user_exp,
    update_user_level,
    set_user_exp_to_zero,
    set_user_level,
)
from core.auto.roles.getters import get_lesser_lvl_roles_list
from core.levels.writers import write_channel_in_config
from core.embeds import construct_basic_embed
from core.errors import (
    construct_error_negative_value_embed,
    construct_error_bot_user_embed,
)
from core.auto.roles.getters import check_level_autorole, get_server_level_autorole, get_autorole_lvl_deletion_state


class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client

    def level_up(self, guild_id, user_id):
        user_exp = get_user_exp(guild_id, user_id)
        user_level = get_user_level(guild_id, user_id)
        leveling_formula = round((7 * (user_level ** 2)) + 58)
        if user_exp >= leveling_formula:
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if get_channel_level_state(message.guild.id, message.channel.id) is False:
            return
        elif self.level_up(message.guild.id, message.author.id):
            update_user_level(message.guild.id, message.author.id, 1)
            set_user_exp_to_zero(message.guild.id, message.author.id)
            user_level = get_user_level(message.guild.id, message.author.id)
            if check_level_autorole(message.guild.id, user_level) is True:
                role = get_server_level_autorole(message.guild.id, user_level)
                role = nextcord.utils.get(message.guild.roles, id=role)
                await message.author.add_roles(role)
                if get_autorole_lvl_deletion_state(message.guild.id) is True:
                    roles_list = get_lesser_lvl_roles_list(message.guild.id, user_level)
                    for rolee in roles_list:
                        try:
                            role = nextcord.utils.get(message.author.guild.roles, id=rolee[0])
                            await message.author.remove_roles(role)
                        except Exception as error:
                            print(error)
            if get_guild_messages_state(message.guild.id) is True:
                user_level = get_user_level(message.guild.id, message.author.id)
                msg = get_msg_from_locale_by_key(message.guild.id, "level_up")
                embed = construct_basic_embed(
                    f"{message.author}",
                    f"{msg}",
                    f"{user_level}:" f"0/{round((7 * (user_level ** 2)) + 58)}",
                    message.author.display_avatar,
                    message.guild.id,
                )
                await message.channel.send(embed=embed)
            else:
                pass
        else:
            min_exp, max_exp = get_min_max_exp(message.guild.id)
            update_user_exp(message.guild.id, message.author.id, min_exp, max_exp)

    @nextcord.slash_command(
        name="level",
        description="shows information about user's level",
        name_localizations=get_localized_name("level"),
        description_localizations=get_localized_description("level"),
        default_member_permissions=Permissions(send_messages=True),
    )
    @cooldowns.cooldown(1, 5, bucket=cooldowns.SlashBucket.author)
    async def __level(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(required=False),
    ):
        if user is None:
            user = interaction.user
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        await interaction.response.defer()
        user_exp = get_user_exp(interaction.guild.id, user.id)
        user_level = get_user_level(interaction.guild.id, user.id)
        exp_to_next_level = round((7 * (user_level ** 2)) + 58)
        percentage = int(((user_exp * 100) / exp_to_next_level))
        background = Editor(Canvas((900, 300), color="#141414"))
        avatar = BytesIO()
        await user.display_avatar.with_format("png").save(avatar)
        profile_picture = Image.open(avatar)
        profile = Editor(profile_picture).resize((150, 150)).rounded_corners()
        larger_font = Font.montserrat(size=35)
        font = Font.montserrat(size=30)

        card_right_shape = [(650, 0), (750, 300), (900, 300), (900, 0)]

        background.polygon(card_right_shape, color="#FFFFFF")
        background.paste(profile, (30, 30))
        background.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=100,
            color="#FFFFFF",
            radius=150,
        )
        if percentage > 1:
            background.bar(
                (30, 220),
                max_width=650,
                height=40,
                percentage=percentage,
                color="#5865F2",
                radius=20,
            )
        background.text((200, 40), str(user), font=larger_font, color="#FFFFFF")
        background.rectangle((200, 100), width=350, height=2, fill="#FFFFFF")
        lvl_text = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        background.text(
            (200, 130),
            f"{lvl_text} - {user_level} | XP - {user_exp}/{exp_to_next_level}",
            font=font,
            color="#FFFFFF",
        )
        file = nextcord.File(fp=background.image_bytes, filename="levelcard.png")
        await interaction.followup.send(file=file)

    @nextcord.slash_command(
        name="add_exp",
        description="Add to @user some exp",
        name_localizations=get_localized_name("add_exp"),
        description_localizations=get_localized_description("add_exp"),
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __add_exp(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
            exp_points: Optional[int] = SlashOption(
                required=True,
                description="Number of experience points to add",
                description_localizations={
                    "ru": "Количество очков опыта, которые необходимо добавить"
                },
            ),
    ):
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        if exp_points <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    exp_points,
                )
            )
        min_exp, max_exp = exp_points, exp_points
        update_user_exp(interaction.guild.id, user.id, min_exp, max_exp)
        user_level = get_user_level(interaction.guild.id, user.id)
        user_exp = get_user_exp(interaction.guild.id, user.id)
        if user_exp > 0:
            leveling_formula = round((7 * (user_level ** 2)) + 58)
            while self.level_up(interaction.guild.id, interaction.user.id):
                update_user_exp(
                    interaction.guild.id,
                    interaction.user.id,
                    -leveling_formula,
                    -leveling_formula,
                )
                update_user_level(interaction.guild.id, interaction.user.id, 1)
                user_level = get_user_level(interaction.guild.id, user.id)
                if check_level_autorole(interaction.guild.id, user_level) is True:
                    role = get_server_level_autorole(interaction.guild.id, user_level)
                    role = nextcord.utils.get(interaction.guild.roles, id=role)
                    await user.add_roles(role)
                    if get_autorole_lvl_deletion_state(interaction.guild.id) is True:
                        roles_list = get_lesser_lvl_roles_list(interaction.guild.id, user_level)
                        for rolee in roles_list:
                            try:
                                role = nextcord.utils.get(interaction.guild.roles, id=rolee[0])
                                await user.remove_roles(role)
                            except:
                                pass
                leveling_formula = round((7 * (user_level ** 2)) + 58)
        msg = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        msg_2 = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}_2"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{msg} {user.mention} **{exp_points}** {msg_2}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="remove_exp",
        description="remove from @user some exp",
        name_localizations=get_localized_name("remove_exp"),
        description_localizations=get_localized_description("remove_exp"),
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __remove_exp(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
            exp_points: Optional[int] = SlashOption(
                required=True,
                description="Number of experience points to add",
                description_localizations={
                    "ru": "Количество очков опыта, которые необходимо добавить"
                },
            ),
    ):
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        if exp_points <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    exp_points,
                )
            )
        min_exp, max_exp = exp_points, exp_points
        update_user_exp(interaction.guild.id, user.id, -min_exp, -max_exp)
        msg = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        msg_2 = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}_2"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{msg} {user.mention} **{exp_points}** {msg_2}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="reset_level",
        description="Reset level of @User to 1st level 0 exp",
        name_localizations=get_localized_name("reset_level"),
        description_localizations=get_localized_description("reset_level"),
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __reset_level(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
    ):
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        set_user_exp_to_zero(interaction.guild.id, user.id)
        set_user_level(interaction.guild.id, user.id, 1)
        msg = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{msg} {user.mention}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(name="leveling_channel",
                            description="Turn on or turn off exp gain in channel",
                            name_localizations=get_localized_name("leveling_channel"),
                            description_localizations=get_localized_description("leveling_channel"),
                            default_member_permissions=Permissions(administrator=True)
                            )
    async def __leveling_channel(self, interaction: Interaction,
                                 channel: Optional[GuildChannel] = SlashOption(required=True),
                                 enabled: Optional[bool] = SlashOption(required=True)):
        write_channel_in_config(interaction.guild.id, channel.id, enabled)
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


def setup(client):
    client.add_cog(Levels(client))
