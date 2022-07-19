from nextcord.ext import commands

from core.levels.getters import get_user_exp, get_user_level, get_min_max_exp, get_guild_messages_state
from core.levels.updaters import update_user_exp, update_user_level


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
        else:
            min_exp, max_exp = get_min_max_exp(message.guild.id)
            update_user_exp(message.guild.id, message.author.id, min_exp, max_exp)


def setup(client):
    client.add_cog(Levels(client))
