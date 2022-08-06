import nextcord
from nextcord.ext import commands

from core.embeds import construct_log
from core.loggers.getters import get_logging_channel, get_logging_state

LOGGING_CHANNEL_TESTING_ID = 999598199444607016


class EventsLogging(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        if get_logging_channel(message.guild.id) == 0:
            return
        if get_logging_state(message.guild.id) is False:
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
        if get_logging_channel(before.guild.id) == 0:
            return
        if get_logging_state(before.guild.id) is False:
            return
        logging_channel = get_logging_channel(before.guild.id)
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
        if get_logging_channel(member.guild.id) == 0:
            return
        if get_logging_state(member.guild.id) is False:
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
        if get_logging_channel(member.guild.id) == 0:
            return
        if get_logging_state(member.guild.id) is False:
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
        if get_logging_channel(guild.id) == 0:
            return
        if get_logging_state(guild.id) is False:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(embed=construct_log("Member ban", guild, user=user))

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if user.bot:
            return
        if get_logging_channel(guild.id) == 0:
            return
        if get_logging_state(guild.id) is False:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Member unban", guild, user=user)
        )

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if get_logging_channel(before.guild.id) == 0:
            return
        if get_logging_state(before.guild.id) is False:
            return
        if isinstance(before, nextcord.Role):
            if before.position == after.position:
                if before.name == after.name:
                    if before.permissions.value == after.permissions.value:
                        if before.color == after.color:
                            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log(
                "Role update", after.guild, role_before=before, role_after=after
            )
        )

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if get_logging_channel(role.guild.id) == 0:
            return
        if get_logging_state(role.guild.id) is False:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Role create", role.guild, role=role)
        )

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if get_logging_channel(role.guild.id) == 0:
            return
        if get_logging_state(role.guild.id) is False:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Role delete", role.guild, role=role)
        )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if get_logging_channel(channel.guild.id) == 0:
            return
        if get_logging_state(channel.guild.id) is False:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Channel create", channel.guild, channel=channel)
        )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if get_logging_channel(channel.guild.id) == 0:
            return
        if get_logging_state(channel.guild.id) is False:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log("Channel delete", channel.guild, channel=channel)
        )

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if get_logging_channel(before.guild.id) == 0:
            return
        if get_logging_state(before.guild.id) is False:
            return
        logging_channel = LOGGING_CHANNEL_TESTING_ID
        logging_channel = self.client.get_channel(logging_channel)
        await logging_channel.send(
            embed=construct_log(
                "Channel update",
                after.guild,
                channel_before=before,
                channel_after=after,
            )
        )


def setup(client):
    client.add_cog(EventsLogging(client))
