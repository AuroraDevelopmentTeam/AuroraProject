from nextcord.ext import commands
import sqlite3


class Clan:
    def __init__(
        self,
        description,
        role_id,
        level,
        owner,
        members,
        members_limit,
        storage,
        create_date,
        icon,
        image,
        guild_boss,
    ):
        self.description = description
        self.role_id = role_id
        self.level = level
        self.owner = owner
        self.members = members
        self.members_limit = members_limit
        self.storage = storage
        self.create_date = create_date
        self.icon = icon
        self.image = image
        self.guild_boss = guild_boss


class ClanHandler(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(ClanHandler(client))
