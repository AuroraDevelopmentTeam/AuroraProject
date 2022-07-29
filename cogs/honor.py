import random
from typing import Optional

import nextcord
from nextcord.ext import commands
from nextcord import Interaction

from core.honor.getters import get_user_honor_level, get_user_honor_points
from core.honor.updaters import update_honor_level, update_honor_points


def honor_level_up(user_id):
    user_honor_exp = get_user_honor_points(user_id)
    user_honor_level = get_user_honor_level(user_id)
    leveling_formula = round((10000 * user_honor_level))
    if user_honor_exp >= leveling_formula:
        return True
    else:
        return False


class Honor(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction):
        if interaction.user.bot:
            return
        elif honor_level_up(interaction.user.id):
            update_honor_level(interaction.user.id, 1)
        else:
            points = random.randint(0, 2)
            if points > 0:
                update_honor_points(interaction.user.id, points)


def setup(client):
    client.add_cog(Honor(client))
