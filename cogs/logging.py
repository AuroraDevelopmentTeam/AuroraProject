import nextcord
from nextcord.ext import commands

from core.embeds import construct_log

LOGGING_CHANNEL_TESTING_ID = 999598199444607016


class EventsLogging(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log(
                "Message delete",
                message.guild,
                message_channel=message.channel,
                user=message.author,
                message=message,
            )
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log(
                "Message edit",
                after.guild,
                display_message=False,
                message=after,
                jump_url=True,
                message_channel=after.channel,
                user=after.author,
                before=before,
                after=after,
            )
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Member join", member.guild, user=member)
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Member remove", member.guild, user=member)
        )

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if user.bot:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(embed=construct_log("Member ban", guild, user=user))

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if user.bot:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Member unban", guild, user=user)
        )

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log(
                "Role update", after.guild, role_before=before, role_after=after
            )
        )

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Role create", role.guild, role=role)
        )

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Role delete", role.guild, role=role)
        )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Channel create", channel.guild, channel=channel)
        )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Channel create", channel.guild, channel=channel)
        )

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log(
                "Channel create",
                after.guild,
                channel_before=before,
                channel_after=after,
            )
        )


def setup(client):
    client.add_cog(EventsLogging(client))
