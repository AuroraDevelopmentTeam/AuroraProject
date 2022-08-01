from typing import Optional
import locale
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps

from easy_pil import *
import nextcord
from nextcord import Interaction, SlashOption, Permissions
from nextcord.ext import commands
from nextcord.utils import get

from core.checkers import is_married
from core.money.updaters import update_user_balance
from core.money.getters import get_user_balance, get_guild_currency_symbol
from core.marriage.update import marry_users, divorce_users
from core.marriage.create import create_marry_embed, create_marry_yes_embed, create_marry_no_embed, create_love_card, \
    create_love_profile_embed
from core.marriage.getters import get_user_love_description, get_user_marry_date, get_user_pair_id, get_user_like_id, \
    get_user_gifts_price, get_divorce_counter, GIFT_NAMES, GIFT_EMOJIS, GIFT_PRICES
from core.marriage.update import update_user_like, update_user_gift_count, update_user_gift_price, \
    update_user_love_description, update_couple_family_money
from core.embeds import construct_basic_embed
from core.ui.buttons import create_button, ViewAuthorCheck, View
from core.locales.getters import get_msg_from_locale_by_key, get_guild_locale
from core.parsers import parse_likes, parse_user_gifts
from core.embeds import DEFAULT_BOT_COLOR


class Marriage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="marry",
                            description="send marriage request to @User, "
                                        "if marriage will be success you will pay 10000 currency on server",
                            default_member_permissions=Permissions(send_messages=True))
    async def __marry(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True)):
        if user.bot:
            return await interaction.response.send_message('bot_user_error')
        if user == interaction.user:
            return await interaction.response.send_message('self choose error')
        if is_married(interaction.guild.id, interaction.user.id) is True:
            return await interaction.response.send_message('already_married error')
        if is_married(interaction.guild.id, user.id) is True:
            return await interaction.response.send_message('already_married error')
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < 10000:
            return await interaction.response.send_message('not_enough_money_error')
        author = interaction.user
        pair = user

        async def marry_no_callback(interaction: Interaction):
            embed = create_marry_no_embed(interaction.guild.id, author, pair)
            embed.add_field(name='Свадьба неудачна',
                            value=f'Время истекло или пользователь отказался от предложения',
                            inline=False)
            yes_button = create_button("yes", False, True)
            no_button = create_button("no", False, True)
            yes_button.emoji = emoji_yes
            no_button.emoji = emoji_no
            view = View()
            view.add_item(yes_button)
            view.add_item(no_button)
            await interaction.message.edit(embed=embed, view=view)

        async def marry_yes_callback(interaction: Interaction):
            embed = create_marry_yes_embed(interaction.guild.id, author, pair)
            locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
            date_format = "%a, %d %b %Y %H:%M:%S"
            timestamp = datetime.now()
            date = timestamp.strftime(date_format)
            marry_users(interaction.guild.id, author.id, pair.id, date)
            update_user_balance(interaction.guild.id, author.id, -10000)
            yes_button = create_button("yes", False, True)
            no_button = create_button("no", False, True)
            yes_button.emoji = emoji_yes
            no_button.emoji = emoji_no
            view = View()
            view.add_item(yes_button)
            view.add_item(no_button)
            await interaction.message.edit(embed=embed, view=view)

        embed = create_marry_embed(interaction.application_command.name, interaction.guild.id, author, pair)
        emoji_no = get(self.client.emojis, name='emoji_no')
        emoji_yes = get(self.client.emojis, name='emoji_yes')
        yes_button = create_button("yes", marry_yes_callback, False)
        no_button = create_button("no", marry_no_callback, False)
        yes_button.emoji = emoji_yes
        no_button.emoji = emoji_no
        view = ViewAuthorCheck(pair)
        view.add_item(yes_button)
        view.add_item(no_button)
        await interaction.response.send_message(embed=embed, view=view)

    @nextcord.slash_command(name="loveprofile", description="sends your couple love card in chat with some "
                                                            "information about couple!",
                            default_member_permissions=Permissions(send_messages=True))
    async def __loveprofile(self, interaction: Interaction):
        await interaction.response.defer()
        if is_married(interaction.guild.id, interaction.user.id) is False:
            return await interaction.followup.send('not married error')
        pair = await self.client.fetch_user(get_user_pair_id(interaction.guild.id, interaction.user.id))
        avatar = BytesIO()
        await interaction.user.display_avatar.with_format("png").save(avatar)
        user_profile_picture = Image.open(avatar)
        avatar = BytesIO()
        await pair.display_avatar.with_format("png").save(avatar)
        pair_profile_picture = Image.open(avatar)
        file = create_love_card(user_profile_picture, pair_profile_picture)
        embed = create_love_profile_embed(interaction.application_command.name, interaction.guild.id,
                                          interaction.user, pair)
        await interaction.followup.send(embed=embed, file=file)

    @nextcord.slash_command(name="divorce", description="divorce you with your partner",
                            default_member_permissions=Permissions(send_messages=True))
    async def __divorce(self, interaction: Interaction):
        if is_married(interaction.guild.id, interaction.user.id) is False:
            return await interaction.response.send_message('not married error')
        pair_id = get_user_pair_id(interaction.guild.id, interaction.user.id)
        pair = await self.client.fetch_user(pair_id)
        if pair is None:
            pair = "кто-то мне неизвестный"
        else:
            pair = pair.mention
        divorce_users(interaction.guild.id, interaction.user.id, pair_id)
        message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"{interaction.user.mention} {message} {pair}",
                                        f"{requested} {interaction.user}",
                                        interaction.user.display_avatar))

    @nextcord.slash_command(name="waifu", description="Sends your profile waifu description",
                            default_member_permissions=Permissions(send_messages=True))
    async def __waifu(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=False)):
        if user is None:
            user = interaction.user
        if user.bot:
            return await interaction.response.send_message('bot_user_error')
        pair_id = get_user_pair_id(interaction.guild.id, user.id)
        like_id = get_user_like_id(interaction.guild.id, user.id)
        gift_price = get_user_gifts_price(interaction.guild.id, user.id)
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        divorces = get_divorce_counter(interaction.guild.id, user.id)
        likes_counter = parse_likes(interaction.guild.id, user.id)
        gifts = parse_user_gifts(interaction.guild.id, user.id)
        embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
        if pair_id == 0:
            parther = "-"
        else:
            parther = await self.client.fetch_user(pair_id)
            if parther is None:
                parther = "кто-то мне неизвестный"
            else:
                parther = f'{parther.mention}'
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        embed.set_author(name=f"{interaction.application_command.name.capitalize()} - {user}")
        embed.add_field(name="Партнёр", value=parther, inline=True)
        if like_id == 0:
            parther = "-"
        else:
            parther = await self.client.fetch_user(like_id)
            if parther is None:
                parther = "кто-то мне неизвестный"
            else:
                parther = f'{parther.mention}'
        embed.add_field(name="Нравится", value=parther, inline=True)
        embed.add_field(name="Цена", value=f'__**{gift_price}**__ {currency_symbol}', inline=True)
        embed.add_field(name="Разводы", value=divorces, inline=True)
        embed.add_field(name="Симпатии", value=likes_counter, inline=True)
        embed.add_field(name="Подарки", value=gifts, inline=False)
        embed.set_thumbnail(url=user.display_avatar)
        embed.set_footer(text=f"{requested} {interaction.user}", icon_url=interaction.user.display_avatar)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="like", description="Choose user you like and he will appear in /waifu command!",
                            default_member_permissions=Permissions(send_messages=True))
    async def __like(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True)):
        if user.bot:
            return await interaction.response.send_message('bot_user_error')
        if user == interaction.user:
            return await interaction.response.send_message('self choose error')
        update_user_like(interaction.guild.id, interaction.user.id, user.id)
        await interaction.response.send_message('done')

    @nextcord.slash_command(name="unlike", description="change person that you like to noone",
                            default_member_permissions=Permissions(send_messages=True))
    async def __unlike(self, interaction: Interaction):
        update_user_like(interaction.guild.id, interaction.user.id, 0)
        await interaction.response.send_message('done')

    @nextcord.slash_command(name="gifts", description="shows gift shop menu",
                            default_member_permissions=Permissions(send_messages=True))
    async def __gifts(self, interaction: Interaction):
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        guild_locale = get_guild_locale(interaction.guild.id)
        counter = 1
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        embed = nextcord.Embed(color=DEFAULT_BOT_COLOR)
        embed.set_author(name=f"{interaction.application_command.name.capitalize()}")
        for i in range(10):
            gift_now = f"gift_{str(counter)}"
            embed.add_field(name=f"**{counter}**. {GIFT_EMOJIS[gift_now]} {GIFT_NAMES[guild_locale][gift_now]}",
                            value=f"> __**{GIFT_PRICES[gift_now]}**__ {currency_symbol}", inline=True)
            counter += 1
        embed.set_image(
            url="https://64.media.tumblr.com/6b9d5fbcc7d6ebe2c3636ed25a550787/f02e19988b551a66-43/s1280x1920/311bc898f00d0bea349351a7a36333f9f659f645.gifv")
        embed.set_footer(text=f"{requested} {interaction.user}", icon_url=interaction.user.display_avatar)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="gift", description="gift to @User gifts from shop!",
                            default_member_permissions=Permissions(send_messages=True))
    async def __gift(self, interaction: Interaction,
                     user: Optional[nextcord.Member] = SlashOption(required=True),
                     gift: str = SlashOption(
                         name="picker",
                         choices={f"1. Carrot 🥕": "gift_1",
                                  f"2. Teddy Bear 🧸": "gift_2",
                                  f"3. Cookie 🍪": "gift_3",
                                  f"4. Lolipop 🍭": "gift_4",
                                  f"5. Flower 🌸": "gift_5",
                                  f"6. Scarf 🧣": "gift_6",
                                  f"7. Cake 🎂": "gift_7",
                                  f"8. Panda 🐼": "gift_8",
                                  f"9. Duck 🦆": "gift_9",
                                  f"10. Cat 🐱": "gift_10"
                                  },
                         required=True), amount: Optional[int] = SlashOption(required=True)):
        if amount < 1:
            return await interaction.response.send_message('negative_value_error')
        if user.bot:
            return await interaction.response.send_message('bot_user_error')
        if user == interaction.user:
            return await interaction.response.send_message('self choose error')
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        price = GIFT_PRICES[gift] * amount
        if balance < price:
            return await interaction.response.send_message('not_enough_money_error')
        update_user_balance(interaction.guild.id, interaction.user.id, -price)
        update_user_gift_count(interaction.guild.id, user.id, gift, amount)
        update_user_gift_price(interaction.guild.id, user.id, price)
        message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"**{amount}** {GIFT_EMOJIS[gift]} {message} {user.mention}",
                                        f"{requested} {interaction.user}\n{msg} {balance}",
                                        interaction.user.display_avatar))

    @nextcord.slash_command(name="lovedescription", description="set your couple description",
                            default_member_permissions=Permissions(send_messages=True))
    async def __lovedescription(self, interaction: Interaction,
                                description: Optional[str] = SlashOption(required=True)):
        if is_married(interaction.guild.id, interaction.user.id) is False:
            return await interaction.response.send_message('not married error')
        update_user_love_description(interaction.guild.id, interaction.user.id, description)
        await interaction.response.send_message('done')

    @nextcord.slash_command(name="lovedeposit", description="deposit money in your family bank",
                            default_member_permissions=Permissions(send_messages=True))
    async def __lovedeposit(self, interaction: Interaction,
                                amount: Optional[int] = SlashOption(required=True)):
        if is_married(interaction.guild.id, interaction.user.id) is False:
            return await interaction.response.send_message('not married error')
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        if amount <= 0:
            return await interaction.response.send_message('negative_value_error')
        if balance < amount:
            return await interaction.response.send_message('not_enough_money_error')
        pair = get_user_pair_id(interaction.guild.id, interaction.user.id)
        update_user_balance(interaction.guild.id, interaction.user.id, -amount)
        update_couple_family_money(interaction.guild.id, interaction.user.id, pair, amount)
        message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        await interaction.response.send_message(
            embed=construct_basic_embed(interaction.application_command.name,
                                        f"__**{amount}**__ {currency_symbol} {message}",
                                        f"{requested} {interaction.user}\n{msg} {balance}",
                                        interaction.user.display_avatar))


def setup(client):
    client.add_cog(Marriage(client))
