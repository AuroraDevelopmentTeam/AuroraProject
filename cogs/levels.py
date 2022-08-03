from typing import Optional
from easy_pil import *
from PIL import Image
from io import BytesIO

import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction, SlashOption, Permissions

from core.locales.getters import get_msg_from_locale_by_key
from core.levels.getters import (
    get_user_exp,
    get_user_level,
    get_min_max_exp,
    get_guild_messages_state,
)
from core.levels.updaters import (
    update_user_exp,
    update_user_level,
    set_user_exp_to_zero,
    set_user_level,
)
from core.embeds import construct_basic_embed


class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client

    def level_up(self, guild_id, user_id):
        user_exp = get_user_exp(guild_id, user_id)
        user_level = get_user_level(guild_id, user_id)
        leveling_formula = round((7 * (user_level**3)))
        if user_exp >= leveling_formula:
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        elif self.level_up(message.guild.id, message.author.id):
            update_user_level(message.guild.id, message.author.id, 1)
            set_user_exp_to_zero(message.guild.id, message.author.id)
            if get_guild_messages_state(message.guild.id) is True:
                user_level = get_user_level(message.guild.id, message.author.id)
                msg = get_msg_from_locale_by_key(message.guild.id, "level_up")
                embed = construct_basic_embed(
                    f"{message.author}",
                    f"{msg}",
                    f"{user_level}:" f"0/{round((7 * (user_level ** 3)))}",
                    message.author.display_avatar,
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
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __level(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(required=False),
    ):
        if user is None:
            user = interaction.user
        if user.bot:
            return await interaction.response.send_message("bot_user_error")
        user_exp = get_user_exp(interaction.guild.id, user.id)
        user_level = get_user_level(interaction.guild.id, user.id)
        exp_to_next_level = round((7 * (user_level**3)))
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
        background.text(
            (200, 130),
            f"Level - {user_level} | XP - {user_exp}/{exp_to_next_level}",
            font=font,
            color="#FFFFFF",
        )
        file = nextcord.File(fp=background.image_bytes, filename="levelcard.png")
        await interaction.response.send_message(file=file)

    @nextcord.slash_command(
        name="add_exp",
        description="add to @user some exp",
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __add_exp(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(required=True),
        exp_points: Optional[int] = SlashOption(required=True),
    ):
        if user.bot:
            return await interaction.response.send_message("bot_user_error")
        if exp_points <= 0:
            return await interaction.response.send_message("negative_value_error")
        min_exp, max_exp = exp_points, exp_points
        update_user_exp(interaction.guild.id, user.id, min_exp, max_exp)
        await interaction.response.send_message("done")

    @nextcord.slash_command(
        name="remove_exp",
        description="remove from @user some exp",
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __remove_exp(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(required=True),
        exp_points: Optional[int] = SlashOption(required=True),
    ):
        if user.bot:
            return await interaction.response.send_message("bot_user_error")
        if exp_points <= 0:
            return await interaction.response.send_message("negative_value_error")
        min_exp, max_exp = exp_points, exp_points
        update_user_exp(interaction.guild.id, user.id, -min_exp, -max_exp)
        await interaction.response.send_message("done")

    @nextcord.slash_command(
        name="reset_level",
        description="Reset level of @User to 1st level 0 exp",
        default_member_permissions=Permissions(administrator=True),
    )
    @application_checks.has_permissions(manage_guild=True)
    async def __reset_level(
        self,
        interaction: Interaction,
        user: Optional[nextcord.Member] = SlashOption(required=True),
    ):
        if user.bot:
            return await interaction.response.send_message("bot_user_error")
        set_user_exp_to_zero(interaction.guild.id, user.id)
        set_user_level(interaction.guild.id, user.id, 1)
        await interaction.response.send_message("done")


def setup(client):
    client.add_cog(Levels(client))
