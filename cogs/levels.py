from typing import Optional
from easy_pil import *

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Permissions

from core.locales.getters import get_msg_from_locale_by_key
from core.levels.getters import get_user_exp, get_user_level, get_min_max_exp, get_guild_messages_state
from core.levels.updaters import update_user_exp, update_user_level, set_user_exp_to_zero, set_user_level
from core.levels.create import create_card
from core.embeds import construct_basic_embed


class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client

    def level_up(self, guild_id, user_id):
        user_exp = get_user_exp(guild_id, user_id)
        user_level = get_user_level(guild_id, user_id)
        leveling_formula = round((7 * (user_level ** 3)))
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
                msg = get_msg_from_locale_by_key(message.guild.id, 'level_up')
                embed = construct_basic_embed(f'{message.author}',
                                              f"{msg}",
                                              f"{user_level}:"
                                              f"0/{round((7 * (user_level ** 3)))}",
                                              message.author.display_avatar)
                await message.channel.send(embed=embed)
            else:
                pass
        else:
            min_exp, max_exp = get_min_max_exp(message.guild.id)
            update_user_exp(message.guild.id, message.author.id, min_exp, max_exp)

    @nextcord.slash_command(name='level', description="shows information about user's level",
                            default_member_permissions=Permissions(send_messages=True))
    async def __level(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=False)):
        if user is None:
            user = interaction.user
        user_exp = get_user_exp(interaction.guild.id, user.id)
        user_level = get_user_level(interaction.guild.id, user.id)
        exp_to_next_level = round((7 * (user_level ** 3)))
        file = create_card(user, user_level, user_exp, exp_to_next_level)
        await interaction.response.send_message(file=file)

    @nextcord.slash_command(name='add_exp', description="add to @user some exp",
                            default_member_permissions=Permissions(administrator=True))
    async def __add_exp(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                        exp_points: Optional[int] = SlashOption(required=True)):
        min_exp, max_exp = exp_points, exp_points
        update_user_exp(interaction.guild.id, user.id, min_exp, max_exp)
        await interaction.response.send_message('done')

    @nextcord.slash_command(name='remove_exp', description="remove from @user some exp",
                            default_member_permissions=Permissions(administrator=True))
    async def __remove_exp(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                        exp_points: Optional[int] = SlashOption(required=True)):
        min_exp, max_exp = exp_points, exp_points
        update_user_exp(interaction.guild.id, user.id, -min_exp, -max_exp)
        await interaction.response.send_message('done')


def setup(client):
    client.add_cog(Levels(client))
