import sqlite3
import types
import datetime
from typing import Union, Optional

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from nextcord.utils import get

from core.clan.getters import *
from core.clan.update import *
from core.clan.writers import write_clan, write_clan_on_start
from core.money.getters import get_guild_currency_symbol, get_user_balance
from core.money.updaters import update_user_balance
from core.ui.buttons import create_button, ViewAuthorCheck, View
from core.locales.getters import get_localized_name, get_localized_description, get_msg_from_locale_by_key, \
    localize_name, get_guild_locale
from core.embeds import construct_basic_embed, DEFAULT_BOT_COLOR
from core.errors import construct_error_not_enough_embed


async def yes_create(interaction: Interaction):
    await interaction.response.defer()
    create_cost = get_server_clan_create_cost(interaction.guild.id)
    update_user_balance(interaction.guild.id, interaction.user.id, -create_cost)
    clan_id = get_owner_clan_id(interaction.guild.id, interaction.user.id)
    color = get_clan_color(interaction.guild.id, clan_id)
    color_to_table = color
    color = color.replace("#", "")
    col = nextcord.Color(value=int(color, 16))
    col = col.to_rgb()
    name = get_clan_name(interaction.guild.id, clan_id)
    desc = get_clan_description(interaction.guild.id, clan_id)
    icon = get_clan_icon(interaction.guild.id, clan_id)
    create_channels = get_server_create_clan_channels(interaction.guild.id)
    role = await interaction.guild.create_role(name=name, color=nextcord.Color.from_rgb(*col))
    overwrites = {
        interaction.guild.default_role: nextcord.PermissionOverwrite(
            connect=False,
            speak=False
        ),
        role: nextcord.PermissionOverwrite(
            connect=True,
            speak=True
        ),
    }
    if create_channels is not False:
        clan_category = get_server_clan_voice_category(interaction.guild.id)
        if clan_category == 0:
            voice_channel = await interaction.guild.create_voice_channel(category=None, name=name,
                                                                         overwrites=overwrites)
        else:
            try:
                category = nextcord.utils.get(interaction.guild.categories, id=clan_category)
            except:
                category = 0
            if category == 0:
                voice_channel = await interaction.guild.create_voice_channel(category=None, name=name,
                                                                             overwrites=overwrites)
            else:
                voice_channel = await interaction.guild.create_voice_channel(category=category, name=name,
                                                                             overwrites=overwrites)
        voice_channel_id = voice_channel.id
    else:
        voice_channel_id = 0
    await interaction.user.add_roles(role)
    delete_clan(interaction.guild.id, interaction.user.id)
    timestamp = nextcord.utils.format_dt(datetime.datetime.now())
    write_clan(interaction.guild.id, interaction.user.id, timestamp, icon, desc, name, role.id, voice_channel_id,
               color_to_table)
    update_user_clan_id(interaction.guild.id, interaction.user.id, clan_id)
    update_user_join_date(interaction.guild.id, interaction.user.id, timestamp)
    yes_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "yes"), False, True)
    no_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "no"), False, True)
    emoji_no = "<:emoji_no:996720327197458442>"
    emoji_yes = "<:emoji_yes:995604874584657951>"
    yes_button.emoji = emoji_yes
    no_button.emoji = emoji_no
    view = ViewAuthorCheck(interaction.user)
    view.add_item(yes_button)
    view.add_item(no_button)
    embed = nextcord.Embed(
        title=f"Клан", description=f"Восславьте **{name}**! Поздравляем вас основатель {interaction.user.mention}, "
                                   f"прославьте имя своего клана, желаем вам удачи на вашем пути!"
    )
    return await interaction.followup.send(embed=embed, view=view)


async def no_create_guild(interaction: Interaction):
    embed = nextcord.Embed(
        title=f"{localize_name(interaction.guild.id, 'clan_create')}",
        description="Отказ от создания"
    )
    delete_clan(interaction.guild.id, interaction.user.id)
    yes_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "yes"), False, True)
    no_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "no"), False, True)
    emoji_no = "<:emoji_no:996720327197458442>"
    emoji_yes = "<:emoji_yes:995604874584657951>"
    yes_button.emoji = emoji_yes
    no_button.emoji = emoji_no
    view = ViewAuthorCheck(interaction.user)
    view.add_item(yes_button)
    view.add_item(no_button)
    await interaction.message.edit(embed=embed, view=view)


async def yes_create_guild(interaction: Interaction):
    embed = nextcord.Embed(
        title=f"{localize_name(interaction.guild.id, 'clan_create')}",
        description="Отлично, теперь настало время ввести имя Клана"
    )
    yes_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "yes"), False, True)
    no_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "no"), False, True)
    emoji_no = "<:emoji_no:996720327197458442>"
    emoji_yes = "<:emoji_yes:995604874584657951>"
    yes_button.emoji = emoji_yes
    no_button.emoji = emoji_no
    view = ViewAuthorCheck(interaction.user)
    view.add_item(yes_button)
    view.add_item(no_button)
    await interaction.message.edit(embed=embed, view=view)


async def yes_show_me_desc_modal(interaction: Interaction):
    modal = ClanDescriptionModal("DescriptionClan")
    name = await interaction.response.send_modal(modal)
    return name


async def yes_show_me_icon_modal(interaction: Interaction):
    modal = ClanIconModal("IconClan")
    name = await interaction.response.send_modal(modal)
    return name


async def yes_show_me_colors_modal(interaction: Interaction):
    modal = ClanColorModal("Colors")
    name = await interaction.response.send_modal(modal)
    return name


async def yes_show_me_full(interaction: Interaction):
    clan_id = get_owner_clan_id(interaction.guild.id, interaction.user.id)
    name = get_clan_name(interaction.guild.id, clan_id)
    desc = get_clan_description(interaction.guild.id, clan_id)
    color = get_clan_color(interaction.guild.id, clan_id)
    color = color.replace("#", "")
    col = nextcord.Color(value=int(color, 16))
    col = col.to_rgb()
    icon = get_clan_icon(interaction.guild.id, clan_id)
    embed = nextcord.Embed(
        title=name,
        description=f"{desc}\n\n\nЕсли вас всё устраивает, то нажмите да, с вас будут списаны деньги, а клан будет "
                    f"создан, если вы передумали, то нажмите нет и процесс создания клана будет отменён.",
        color=nextcord.Color.from_rgb(*col)
    )
    embed.set_thumbnail(url=icon)
    yes_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "yes"), yes_create,
                               False)
    no_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "no"), no_create_guild,
                              False)
    emoji_no = "<:emoji_no:996720327197458442>"
    emoji_yes = "<:emoji_yes:995604874584657951>"
    yes_button.emoji = emoji_yes
    no_button.emoji = emoji_no
    view = ViewAuthorCheck(interaction.user)
    view.add_item(yes_button)
    view.add_item(no_button)
    return await interaction.message.edit(embed=embed, view=view)


class ClanColorModal(nextcord.ui.Modal):
    def __init__(self, name):
        self.name = name
        super().__init__(
            "Clan Color",
        )
        self.embedTitle = nextcord.ui.TextInput(
            label="Clan Color",
            min_length=7,
            max_length=7,
            required=True,
            placeholder="#010101",
        )
        self.add_item(self.embedTitle)

    async def callback(self, interaction: Interaction):
        try:
            name = self.embedTitle.value
            update_clan_color(interaction.guild.id, interaction.user.id, name)
            color = name
            color = color.replace("#", "")
            col = nextcord.Color(value=int(color, 16))
            col = col.to_rgb()
            embed = nextcord.Embed(
                description=f"Был указан следующий цвет: {name}. "
                            f"Нажмите да, чтоб посмотреть конечный результат или нет, если хотите изменить цвет.",
                color=nextcord.Color.from_rgb(*col)
            )
            yes_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "yes"), yes_show_me_full,
                                       False)
            no_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "no"), yes_show_me_colors_modal,
                                      False)
            emoji_no = "<:emoji_no:996720327197458442>"
            emoji_yes = "<:emoji_yes:995604874584657951>"
            yes_button.emoji = emoji_yes
            no_button.emoji = emoji_no
            view = ViewAuthorCheck(interaction.user)
            view.add_item(yes_button)
            view.add_item(no_button)
            await interaction.message.edit(embed=embed, view=view)
        except Exception as error:
            print(error)
            delete_clan(interaction.guild.id, interaction.user.id)


class ClanIconModal(nextcord.ui.Modal):
    def __init__(self, name):
        self.name = name
        super().__init__(
            "Clan Icon",
        )
        self.embedTitle = nextcord.ui.TextInput(
            label="Clan Icon",
            min_length=22,
            max_length=300,
            required=True,
            placeholder="Clan Icon",
        )
        self.add_item(self.embedTitle)

    async def callback(self, interaction: Interaction):
        try:
            name = self.embedTitle.value
            update_clan_icon_on_creation(interaction.guild.id, interaction.user.id, name)
            embed = nextcord.Embed(
                description=f"Была указана следующая иконка: **{name}**. Теперь необходимо указать цвет вашей гильдии в "
                            f"формате HEX кода. HEX-коды имеют следующий вид: #код и должны быть именно введены в "
                            f"подобном виде, иначе бот выдаст ошибку и процесс создания клана будет прекращён. Если вы "
                            f"абсолютно ничего не понимаете в HEX-кодах и желания гуглить нужный вам цвет у вас нет, "
                            f"то далее приводится список HEX-кодов основных цветов, просто скопируйте и вставьте ("
                            f"ОБЯЗАТЕЛЬНО! вместе с #).\nЧёрный - #000000\nСерый - #808080\nБелый - #FFFFFF\nСеребряный - "
                            f"#C0C0C0\nСиний - #0000FF\nТёмно-синий - #00008B\nЦиан - #00FFFF\nАквамарин - #7FFFD4\n"
                            f"Зелёный - #008000\nЛайм - #00FF00\nФиолетовый - #800080\nФуксия - #FF00FF\n"
                            f"Оливковый - #808000\nКрасный - #FF0000\nЗолотой - #FFD700\nЖелтый - #FFFF00\nОранжевый - "
                            f"#FFA500\nКоралловый - #F08080\nКликните на да, как будете готовы или кликните нет и "
                            f"поменяйте иконку. "
            )
            embed.set_thumbnail(url=name)
            yes_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "yes"),
                                       yes_show_me_colors_modal,
                                       False)
            no_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "no"), yes_show_me_icon_modal,
                                      False)
            emoji_no = "<:emoji_no:996720327197458442>"
            emoji_yes = "<:emoji_yes:995604874584657951>"
            yes_button.emoji = emoji_yes
            no_button.emoji = emoji_no
            view = ViewAuthorCheck(interaction.user)
            view.add_item(yes_button)
            view.add_item(no_button)
            await interaction.message.edit(embed=embed, view=view)
        except Exception as error:
            print(error)
            delete_clan(interaction.guild.id, interaction.user.id)


class ClanDescriptionModal(nextcord.ui.Modal):
    def __init__(self, name):
        self.name = name
        super().__init__(
            "Clan Description",
        )
        self.embedTitle = nextcord.ui.TextInput(
            label="Clan name",
            min_length=100,
            max_length=1600,
            required=True,
            placeholder="Clan description",
            style=nextcord.TextInputStyle.paragraph
        )
        self.add_item(self.embedTitle)

    async def callback(self, interaction: Interaction):
        try:
            name = self.embedTitle.value
            update_clan_desc_on_creation(interaction.guild.id, interaction.user.id, name)
            embed = nextcord.Embed(
                description=f"Было введено следующее описание: **{name}**. Теперь необходимо указать иконку гильдии в "
                            f"формате url ссылки, к примеру: "
                            f"**https://c.tenor.com/o656qFKDzeUAAAAM/rick-astley-never-gonna-give-you-up.gif**, "
                            f"ничего не мешает использовать в качестве иконки и png/jpg изображения, так и гифки, "
                            f"выбирайте то, что вам нравится."
                            f"Кликните на да, как будете готовы или переделайте описание нажав нет."
            )
            embed.set_thumbnail(url="https://c.tenor.com/o656qFKDzeUAAAAM/rick-astley-never-gonna-give-you-up.gif")
            yes_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "yes"), yes_show_me_icon_modal,
                                       False)
            no_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "no"), yes_show_me_desc_modal,
                                      False)
            emoji_no = "<:emoji_no:996720327197458442>"
            emoji_yes = "<:emoji_yes:995604874584657951>"
            yes_button.emoji = emoji_yes
            no_button.emoji = emoji_no
            view = ViewAuthorCheck(interaction.user)
            view.add_item(yes_button)
            view.add_item(no_button)
            await interaction.message.edit(embed=embed, view=view)
        except Exception as error:
            print(error)
            delete_clan(interaction.guild.id, interaction.user.id)


class NameModal(nextcord.ui.Modal):
    def __init__(self, name, client):
        self.client = client
        self.name = name
        super().__init__(
            "Clan name",
        )
        self.embedTitle = nextcord.ui.TextInput(
            label="Clan name",
            min_length=3,
            max_length=100,
            required=True,
            placeholder="Clan name",
        )
        self.add_item(self.embedTitle)

    async def callback(self, interaction: Interaction) -> None:
        try:
            name = self.embedTitle.value
            update_clan_name(interaction.guild.id, interaction.user.id, name)
            embed = nextcord.Embed(
                description=f"Было введено следующее имя клана: **{name}**. Теперь введите описание для вашего клана, "
                            f"кликните на да, как будете готовы или прекратите процесс создания если передумали, "
                            f"нажав нет. "
            )
            yes_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "yes"), yes_show_me_desc_modal,
                                       False)
            no_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "no"), no_create_guild, False)
            emoji_no = "<:emoji_no:996720327197458442>"
            emoji_yes = "<:emoji_yes:995604874584657951>"
            yes_button.emoji = emoji_yes
            no_button.emoji = emoji_no
            view = ViewAuthorCheck(interaction.user)
            view.add_item(yes_button)
            view.add_item(no_button)
            await interaction.message.edit(embed=embed, view=view)
        except Exception as error:
            print(error)
            delete_clan(interaction.guild.id, interaction.user.id)


class Clan:
    def __init__(self, description, role_id, level, owner, members, members_limit, storage, create_date, icon, image,
                 guild_boss):
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

    @nextcord.slash_command(name="clan", description="User menu of creating clans")
    async def __clan(self, interaction: Interaction):
        pass

    @__clan.subcommand(name="create", description="Creating a clan")
    async def __clan_create(self, interaction: Interaction):
        create_cost = get_server_clan_create_cost(interaction.guild.id)
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < create_cost:
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            return await interaction.response.send_message(
                embed=construct_error_not_enough_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_enough_money_error"
                    ),
                    interaction.user.display_avatar,
                    f"{msg} {balance}/{create_cost}",
                )
            )
        await interaction.response.defer()
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"clan_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")

        async def yes_show_me_name_modal_(interaction: Interaction):
            modal = NameModal("NameClan", self.client)
            name = await interaction.response.send_modal(modal)
            print(name)
            return name

        async def yes_create_guild_(interaction: Interaction):
            write_clan_on_start(interaction.guild.id, interaction.user.id)
            embed = nextcord.Embed(
                title=f"{localize_name(interaction.guild.id, 'clan_create')}",
                description="Отлично, теперь настало время ввести имя Клана"
            )
            yes_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "yes"), yes_show_me_name_modal_,
                                       False)
            no_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "no"), no_create_guild_, False)
            yes_button.emoji = emoji_yes
            no_button.emoji = emoji_no
            view = ViewAuthorCheck(interaction.user)
            view.add_item(yes_button)
            view.add_item(no_button)
            name = await interaction.message.edit(embed=embed, view=view)

        async def no_create_guild_(interaction: Interaction):
            embed = nextcord.Embed(
                title=f"{localize_name(interaction.guild.id, 'clan_create')}",
                description="Отказ от создания"
            )
            yes_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "yes"), False, True)
            no_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "no"), False, True)
            yes_button.emoji = emoji_yes
            no_button.emoji = emoji_no
            view = ViewAuthorCheck(interaction.user)
            view.add_item(yes_button)
            view.add_item(no_button)
            await interaction.message.edit(embed=embed, view=view)

        emoji_no = get(self.client.emojis, name="emoji_no")
        emoji_yes = get(self.client.emojis, name="emoji_yes")
        yes_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "yes"), yes_create_guild_, False)
        no_button = create_button(get_msg_from_locale_by_key(interaction.guild.id, "no"), no_create_guild_, False)
        yes_button.emoji = emoji_yes
        no_button.emoji = emoji_no
        view = ViewAuthorCheck(interaction.user)
        view.add_item(yes_button)
        view.add_item(no_button)
        await interaction.followup.send(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} **{create_cost}** {currency_symbol}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar, interaction.guild.id
            )
            ,
            view=view
        )

    @__clan.subcommand(name="display", description="Displaying your clan")
    async def __clan_display(self, interaction: Interaction):
        await interaction.response.defer()
        clan_id = get_user_clan_id(interaction.guild.id, interaction.user.id)
        clan_description = get_clan_description(interaction.guild.id, clan_id)
        clan_name = get_clan_name(interaction.guild.id, clan_id)
        clan_level = get_clan_level(interaction.guild.id, clan_id)
        clan_exp = get_clan_exp(interaction.guild.id, clan_id)
        role = get_clan_role(interaction.guild.id, clan_id)
        storage = get_clan_storage(interaction.guild.id, clan_id)
        members = fetchall_clan_members(interaction.guild.id, clan_id)
        limit = get_clan_member_limit(interaction.guild.id, clan_id)
        role = nextcord.utils.get(interaction.guild.roles, id=role)
        created = get_clan_create_date(interaction.guild.id, clan_id)
        join_date = get_user_join_date(interaction.guild.id, interaction.user.id, clan_id)
        guild_boss = get_clan_guild_boss_level(interaction.guild.id, clan_id)
        full_hp = guild_boss * 100
        guild_boss_hp = get_clan_guild_boss_hp(interaction.guild.id, clan_id)
        color = get_clan_color(interaction.guild.id, clan_id)
        clan_icon = get_clan_icon(interaction.guild.id, clan_id)
        clan_owner = get_clan_owner_id(interaction.guild.id, clan_id)
        clan_owner = nextcord.utils.get(interaction.guild.members, id=clan_owner)
        color = color.replace("#", "")
        col = nextcord.Color(value=int(color, 16))
        col = col.to_rgb()
        embed = nextcord.Embed(
            title=f"{clan_name} - {interaction.user.name}",
            description=f"**Описание клана**:\n{clan_description}",
            color=nextcord.Color.from_rgb(*col)
        )
        embed.set_thumbnail(url=clan_icon)
        embed.add_field(name="Владелец", value=f"{clan_owner.mention}", inline=True)
        embed.add_field(name="Участники", value=f"{len(members)}/{limit}", inline=True)
        embed.add_field(name="Роль", value=f"{role.mention}", inline=True)
        embed.add_field(name="Банк клана", value=f"{storage}", inline=True)
        embed.add_field(name="Уровень", value=f"**{clan_level}**\n{clan_exp}|28", inline=True)
        embed.add_field(name="Дата основания", value=f"{created}", inline=True)
        embed.add_field(name="Вы присоединились", value=f"{join_date}", inline=True)
        embed.add_field(name="Клановый босс", value=f"Уровень: **{guild_boss}**\nHP: {guild_boss_hp}/{full_hp}",
                        inline=False)
        await interaction.followup.send(embed=embed)

    @__clan.subcommand(name="shop", description="Sends your clan shop with upgrades")
    async def __clan_shop(self, interaction: Interaction):
        pass

    @__clan.subcommand(name="deposit", description="Deposit your money in clan bank")
    async def __clan_deposit(self, interaction: Interaction, money: Optional[int] = SlashOption(required=True)):
        pass

    @__clan.subcommand(name="leave", description="Leave from clan")
    async def __clan_leave(self, interaction: Interaction):
        pass

    @__clan.subcommand(name="invite", description="Send invite in your clan to user")
    async def __clan_invite(self, interaction: Interaction,
                            user: Optional[nextcord.Member] = SlashOption(required=True)):
        pass


def setup(client):
    client.add_cog(ClanHandler(client))
