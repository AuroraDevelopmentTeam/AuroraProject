import nextcord
from typing import Optional
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from config import settings
import sqlite3
from core.locales.updaters import update_guild_locale
from core.checkers import is_locale_valid


class System(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(System(client))
