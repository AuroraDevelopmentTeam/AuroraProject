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
from nextcord.abc import GuildChannel

from core.locales.getters import get_localized_name, get_localized_description
from core.checkers import is_married
from core.money.updaters import update_user_balance
from core.money.getters import get_user_balance, get_guild_currency_symbol
from core.marriage.update import marry_users, divorce_users
from core.marriage.create import (
    create_marry_embed,
    create_marry_yes_embed,
    create_marry_no_embed,
    create_love_card,
    create_love_profile_embed,
)
from core.marriage.getters import (
    get_user_love_description,
    get_user_marry_date,
    get_user_pair_id,
    get_user_like_id,
    get_user_gifts_price,
    get_divorce_counter,
    GIFT_NAMES,
    GIFT_EMOJIS,
    GIFT_PRICES,
    get_marriage_config_enable_loverooms,
    get_marriage_config_marriage_price,
    get_marriage_config_loveroom_category,
    get_marriage_config_month_loveroom_price,
    get_user_loveroom_expire_date,
    get_user_loveroom_id,
    get_family_money,
)
from core.marriage.update import (
    update_user_like,
    update_user_gift_count,
    update_user_gift_price,
    update_user_love_description,
    update_couple_family_money,
    update_marriage_config_enable_loverooms,
    update_marriage_config_loveroom_category,
    update_marriage_config_marriage_price,
    update_marriage_config_month_loveroom_price,
    update_user_loveroom_expire_date,
    update_user_loveroom_id,
)
from core.embeds import construct_basic_embed
from core.ui.buttons import create_button, ViewAuthorCheck, View
from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_guild_locale,
    localize_name,
)
from core.auto.roles.getters import get_server_marriage_autorole
from core.parsers import parse_likes, parse_user_gifts
from core.embeds import DEFAULT_BOT_COLOR
from core.errors import (
    construct_error_negative_value_embed,
    construct_error_bot_user_embed,
    construct_error_self_choose_embed,
    construct_error_not_enough_embed,
    construct_error_already_married_embed,
    construct_error_not_married_embed,
)
from core.emojify import (
    SHOP,
    STAR,
    SWORD,
    SETTINGS,
    HANDWRITTEN_HEARTS,
    HEARTS_SCROLL,
    HEARTS_MANY,
    HEARTS_THREE,
    USERS,
    GIFT,
    MASK,
    RINGS,
    BROKEN_HEART,
    MESSAGE,
    PIGBANK,
    PRICE_TAG,
    VOICE,
    MARRY,
)


class Marriage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="marry",
        description="send marriage request to @User, "
                    "if marriage will be success you will pay 10000 currency on server",
        name_localizations=get_localized_name("marry"),
        description_localizations=get_localized_description("marry"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __marry(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
    ):
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        if user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        if is_married(interaction.guild.id, interaction.user.id) is True:
            return await interaction.response.send_message(
                embed=construct_error_already_married_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "already_married_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        if is_married(interaction.guild.id, user.id) is True:
            return await interaction.response.send_message(
                embed=construct_error_already_married_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "already_married_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        marriage_price = get_marriage_config_marriage_price(interaction.guild.id)
        if balance < marriage_price:
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            return await interaction.response.send_message(
                embed=construct_error_not_enough_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_enough_money_error"
                    ),
                    interaction.user.display_avatar,
                    f"{msg} {balance}/{marriage_price}",
                )
            )
        author = interaction.user
        pair = user

        async def marry_no_callback(interaction: Interaction):
            embed = create_marry_no_embed(interaction.guild.id, author, pair)
            embed.add_field(
                name=f"{emoji_no} Свадьба неудачна",
                value=f"Время истекло или пользователь отказался от предложения",
                inline=False,
            )
            yes_button = create_button(
                get_msg_from_locale_by_key(interaction.guild.id, "yes"), False, True
            )
            no_button = create_button(
                get_msg_from_locale_by_key(interaction.guild.id, "no"), False, True
            )
            yes_button.emoji = emoji_yes
            no_button.emoji = emoji_no
            view = View()
            view.add_item(yes_button)
            view.add_item(no_button)
            await interaction.message.edit(embed=embed, view=view)

        async def marry_yes_callback(interaction: Interaction):
            embed = create_marry_yes_embed(interaction.guild.id, author, pair)
            if get_guild_locale(interaction.guild.id) == "ru_ru":
                locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
            else:
                locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
            date_format = "%a, %d %b %Y %H:%M:%S"
            timestamp = datetime.now()
            date = timestamp.strftime(date_format)
            marry_users(interaction.guild.id, author.id, pair.id, date)
            update_user_balance(interaction.guild.id, author.id, -marriage_price)
            marriage_autorole = get_server_marriage_autorole(interaction.guild.id)
            if marriage_autorole != 0:
                role = nextcord.utils.get(interaction.guild.roles, id=marriage_autorole[0])
                if role != 0:
                    try:
                        await author.add_roles(role)
                        await pair.add_roles(role)
                    except Exception as err:
                        print(err)
            yes_button = create_button(
                get_msg_from_locale_by_key(interaction.guild.id, "yes"), False, True
            )
            no_button = create_button(
                get_msg_from_locale_by_key(interaction.guild.id, "no"), False, True
            )
            yes_button.emoji = emoji_yes
            no_button.emoji = emoji_no
            view = View()
            view.add_item(yes_button)
            view.add_item(no_button)
            await interaction.message.edit(embed=embed, view=view)

        embed = create_marry_embed(
            interaction.application_command.name, interaction.guild.id, author, pair
        )
        emoji_no = get(self.client.emojis, name="emoji_no")
        emoji_yes = get(self.client.emojis, name="emoji_yes")
        yes_button = create_button(
            get_msg_from_locale_by_key(interaction.guild.id, "yes"),
            marry_yes_callback,
            False,
        )
        no_button = create_button(
            get_msg_from_locale_by_key(interaction.guild.id, "no"),
            marry_no_callback,
            False,
        )
        yes_button.emoji = emoji_yes
        no_button.emoji = emoji_no
        view = ViewAuthorCheck(pair)
        view.add_item(yes_button)
        view.add_item(no_button)
        await interaction.response.send_message(embed=embed, view=view)

    @nextcord.slash_command(
        name="loveprofile",
        description="sends your couple love card in chat with some "
                    "information about couple!",
        name_localizations=get_localized_name("loveprofile"),
        description_localizations=get_localized_description("loveprofile"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __loveprofile(self, interaction: Interaction):
        await interaction.response.defer()
        if is_married(interaction.guild.id, interaction.user.id) is False:
            return await interaction.followup.send(
                embed=construct_error_not_married_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_married_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        pair = await self.client.fetch_user(
            get_user_pair_id(interaction.guild.id, interaction.user.id)
        )
        avatar = BytesIO()
        await interaction.user.display_avatar.with_format("png").save(avatar)
        user_profile_picture = Image.open(avatar)
        avatar = BytesIO()
        await pair.display_avatar.with_format("png").save(avatar)
        pair_profile_picture = Image.open(avatar)
        file = create_love_card(user_profile_picture, pair_profile_picture)
        embed = create_love_profile_embed(
            interaction.application_command.name,
            interaction.guild.id,
            interaction.user,
            pair,
        )
        await interaction.followup.send(embed=embed, file=file)

    @nextcord.slash_command(
        name="divorce",
        description="divorce you with your partner",
        name_localizations=get_localized_name("divorce"),
        description_localizations=get_localized_description("divorce"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __divorce(self, interaction: Interaction):
        if is_married(interaction.guild.id, interaction.user.id) is False:
            return await interaction.response.send_message(
                embed=construct_error_not_married_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_married_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        pair_id = get_user_pair_id(interaction.guild.id, interaction.user.id)
        try:
            pair = await interaction.guild.fetch_member(pair_id)
        except nextcord.NotFound:
            pair = None
        divorce_users(interaction.guild.id, interaction.user.id, pair_id)
        marriage_autorole = get_server_marriage_autorole(interaction.guild.id)
        if marriage_autorole != 0:
            role = nextcord.utils.get(interaction.guild.roles, id=marriage_autorole[0])
            if role != 0:
                try:
                    await interaction.user.remove_roles(role)
                    if pair is not None:
                        await pair.remove_roles(role)
                except Exception as error:
                    print(error)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if pair is None:
            pair = get_msg_from_locale_by_key(interaction.guild.id, "unknown_user")
        else:
            pair = pair.mention
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{interaction.user.mention} {message} {pair}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="waifu",
        description="Sends your profile waifu description",
        name_localizations=get_localized_name("waifu"),
        description_localizations=get_localized_description("waifu"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __waifu(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=False,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
    ):
        if user is None:
            user = interaction.user
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        pair_id = get_user_pair_id(interaction.guild.id, user.id)
        like_id = get_user_like_id(interaction.guild.id, user.id)
        gift_price = get_user_gifts_price(interaction.guild.id, user.id)
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        divorces = get_divorce_counter(interaction.guild.id, user.id)
        likes_counter = parse_likes(interaction.guild.id, user.id)
        gifts = parse_user_gifts(interaction.guild.id, user.id)
        embed = nextcord.Embed(
            color=DEFAULT_BOT_COLOR,
            title=f"{HEARTS_SCROLL} {localize_name(interaction.guild.id, interaction.application_command.name).capitalize()} - {user}",
        )
        if pair_id == 0:
            parther = "-"
        else:
            parther = await self.client.fetch_user(pair_id)
            if parther is None:
                parther = get_msg_from_locale_by_key(
                    interaction.guild.id, "unknown_user"
                )
            else:
                parther = f"{parther.mention}"
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        partner_msg = get_msg_from_locale_by_key(interaction.guild.id, "partner")
        embed.add_field(name=f"{RINGS} {partner_msg}", value=parther, inline=True)
        if like_id == 0:
            parther = "-"
        else:
            parther = await self.client.fetch_user(like_id)
            if parther is None:
                parther = "кто-то мне неизвестный"
            else:
                parther = f"{parther.mention}"
        like_msg = get_msg_from_locale_by_key(interaction.guild.id, "ilike")
        price_msg = get_msg_from_locale_by_key(interaction.guild.id, "price")
        embed.add_field(
            name=f"{HANDWRITTEN_HEARTS} {like_msg}", value=parther, inline=True
        )
        embed.add_field(
            name=f"{PRICE_TAG} {price_msg}",
            value=f"__**{gift_price}**__ {currency_symbol}",
            inline=True,
        )
        divorces_msg = get_msg_from_locale_by_key(interaction.guild.id, "divorces")
        likes_msg = get_msg_from_locale_by_key(interaction.guild.id, "likes")
        gifts_msg = get_msg_from_locale_by_key(interaction.guild.id, "gifts")
        embed.add_field(
            name=f"{BROKEN_HEART} {divorces_msg}", value=divorces, inline=True
        )
        embed.add_field(
            name=f"{HEARTS_MANY} {likes_msg}", value=likes_counter, inline=True
        )
        embed.add_field(name=f"{GIFT} {gifts_msg}", value=gifts, inline=False)
        embed.set_thumbnail(url=user.display_avatar)
        embed.set_footer(
            text=f"{requested} {interaction.user}",
            icon_url=interaction.user.display_avatar,
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/772385814483173398/1009395738758893578/808536e504da54a3522fcaa2a4e209e7.gif"
        )
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="like",
        description="Choose user you like and he will appear in /waifu command!",
        name_localizations=get_localized_name("like"),
        description_localizations=get_localized_description("like"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __like(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
    ):
        if user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        update_user_like(interaction.guild.id, interaction.user.id, user.id)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} {user.mention}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="unlike",
        description="change person that you like to noone",
        name_localizations=get_localized_name("unlike"),
        description_localizations=get_localized_description("unlike"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __unlike(self, interaction: Interaction):
        like_id = get_user_like_id(interaction.guild.id, interaction.user.id)
        if like_id == 0:
            embed = nextcord.Embed(
                title="error",
                description=get_msg_from_locale_by_key(
                    interaction.guild.id, "already_like_noone"
                ),
                color=DEFAULT_BOT_COLOR,
            )
            return await interaction.response.send_message(embed=embed)
        update_user_like(interaction.guild.id, interaction.user.id, 0)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="gifts",
        description="shows gift shop menu",
        name_localizations=get_localized_name("gifts"),
        description_localizations=get_localized_description("gifts"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __gifts(self, interaction: Interaction):
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        guild_locale = get_guild_locale(interaction.guild.id)
        counter = 1
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = nextcord.Embed(
            color=DEFAULT_BOT_COLOR,
            title=f"{GIFT} {localize_name(interaction.guild.id, interaction.application_command.name).capitalize()}",
        )
        for i in range(10):
            gift_now = f"gift_{str(counter)}"
            embed.add_field(
                name=f"**{counter}**. {GIFT_EMOJIS[gift_now]} {GIFT_NAMES[guild_locale][gift_now]}",
                value=f"> __**{GIFT_PRICES[gift_now]}**__ {currency_symbol}",
                inline=True,
            )
            counter += 1
        embed.set_image(
            url="https://64.media.tumblr.com/6b9d5fbcc7d6ebe2c3636ed25a550787/f02e19988b551a66-43/s1280x1920/311bc898f00d0bea349351a7a36333f9f659f645.gifv"
        )
        embed.set_footer(
            text=f"{requested} {interaction.user}",
            icon_url=interaction.user.display_avatar,
        )
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="gift",
        description="Gift to @User gifts from shop!",
        name_localizations=get_localized_name("gift"),
        description_localizations=get_localized_description("gift"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __gift(
            self,
            interaction: Interaction,
            user: Optional[nextcord.Member] = SlashOption(
                required=True,
                description="The discord's user, tag someone with @",
                description_localizations={
                    "ru": "Пользователь дискорда, укажите кого-то @"
                },
            ),
            gift: str = SlashOption(
                name="picker",
                choices={
                    f"1. Carrot 🥕": "gift_1",
                    f"2. Teddy Bear 🧸": "gift_2",
                    f"3. Cookie 🍪": "gift_3",
                    f"4. Lolipop 🍭": "gift_4",
                    f"5. Flower 🌸": "gift_5",
                    f"6. Scarf 🧣": "gift_6",
                    f"7. Cake 🎂": "gift_7",
                    f"8. Panda 🐼": "gift_8",
                    f"9. Duck 🦆": "gift_9",
                    f"10. Cat 🐱": "gift_10",
                },
                choice_localizations={
                    "ru": {
                        f"1. Морковка 🥕": "gift_1",
                        f"2. Мишка 🧸": "gift_2",
                        f"3. Печенька 🍪": "gift_3",
                        f"4. Лолипоп 🍭": "gift_4",
                        f"5. Цветочек 🌸": "gift_5",
                        f"6. Шарфик 🧣": "gift_6",
                        f"7. Тортик 🎂": "gift_7",
                        f"8. Панда 🐼": "gift_8",
                        f"9. Утка 🦆": "gift_9",
                        f"10. Кошка 🐱": "gift_10",
                    }
                },
                required=True,
            ),
            amount: Optional[int] = SlashOption(required=True),
    ):
        if amount < 1:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )
        if user.bot:
            return await interaction.response.send_message(
                embed=construct_error_bot_user_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "bot_user_error"),
                    self.client.user.avatar.url,
                )
            )
        if user == interaction.user:
            return await interaction.response.send_message(
                embed=construct_error_self_choose_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "self_choose_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        price = GIFT_PRICES[gift] * amount
        if balance < price:
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            return await interaction.response.send_message(
                embed=construct_error_not_enough_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_enough_money_error"
                    ),
                    interaction.user.display_avatar,
                    f"{msg} {balance}",
                )
            )
        update_user_balance(interaction.guild.id, interaction.user.id, -price)
        update_user_gift_count(interaction.guild.id, user.id, gift, amount)
        update_user_gift_price(interaction.guild.id, user.id, price)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"**{amount}** {GIFT_EMOJIS[gift]} {message} {user.mention}",
                f"{requested} {interaction.user}\n{msg} {balance}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="lovedescription",
        description="Set your couple description",
        name_localizations=get_localized_name("lovedescription"),
        description_localizations=get_localized_description("lovedescription"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __lovedescription(
            self,
            interaction: Interaction,
            description: Optional[str] = SlashOption(required=True),
    ):
        if is_married(interaction.guild.id, interaction.user.id) is False:
            return await interaction.response.send_message(
                embed=construct_error_not_married_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_married_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        update_user_love_description(
            interaction.guild.id, interaction.user.id, description
        )
        message = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"{message} {description}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(
        name="lovedeposit",
        description="Deposit money in your family bank",
        name_localizations=get_localized_name("lovedeposit"),
        description_localizations=get_localized_description("lovedeposit"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __lovedeposit(
            self,
            interaction: Interaction,
            amount: Optional[int] = SlashOption(required=True),
    ):
        if is_married(interaction.guild.id, interaction.user.id) is False:
            return await interaction.response.send_message(
                embed=construct_error_not_married_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_married_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        if amount <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    money,
                )
            )
        if balance < amount:
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            return await interaction.response.send_message(
                embed=construct_error_not_enough_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_enough_money_error"
                    ),
                    interaction.user.display_avatar,
                    f"{msg} {balance}",
                )
            )
        pair = get_user_pair_id(interaction.guild.id, interaction.user.id)
        update_user_balance(interaction.guild.id, interaction.user.id, -amount)
        update_couple_family_money(
            interaction.guild.id, interaction.user.id, pair, amount
        )
        message = get_msg_from_locale_by_key(
            interaction.guild.id, interaction.application_command.name
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        await interaction.response.send_message(
            embed=construct_basic_embed(
                interaction.application_command.name,
                f"__**{amount}**__ {currency_symbol} {message}",
                f"{requested} {interaction.user}\n{msg} {balance}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(name="marriage_config",
                            name_localizations=get_localized_name("marriage_config"),
                            description_localizations=get_localized_description("marriage_config"),
                            default_member_permissions=Permissions(administrator=True),
                            )
    async def __marriage_config(self, interaction: Interaction):
        pass

    @__marriage_config.subcommand(name="enable_loverooms",
                                  name_localizations=get_localized_name("marriage_config_enable_loverooms"),
                                  description_localizations=get_localized_description(
                                      "marriage_config_enable_loverooms"),
                                  )
    async def __marriage_config_enable_loverooms(self, interaction: Interaction,
                                                 enable_loverooms: Optional[bool] = SlashOption(required=True)):
        update_marriage_config_enable_loverooms(interaction.guild.id, enable_loverooms)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"marriage_config_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        if enable_loverooms is True:
            enable_loverooms = get_msg_from_locale_by_key(
                interaction.guild.id, "enabled"
            )
        else:
            enable_loverooms = get_msg_from_locale_by_key(
                interaction.guild.id, "disabled"
            )
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"marriage_config_{interaction.application_command.name}",
                f"{message} **{enable_loverooms}**",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__marriage_config.subcommand(name="marriage_price",
                                  name_localizations=get_localized_name("marriage_config_marriage_price"),
                                  description_localizations=get_localized_description("marriage_config_marriage_price"),
                                  )
    async def __marriage_config_marriage_price(self, interaction: Interaction,
                                               marriage_price: Optional[int] = SlashOption(required=True)):
        if marriage_price <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    marriage_price,
                )
            )
        update_marriage_config_marriage_price(interaction.guild.id, marriage_price)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"marriage_config_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"marriage_config_{interaction.application_command.name}",
                f"{message} **{marriage_price}** {currency_symbol}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__marriage_config.subcommand(name="month_loveroom_price",
                                  name_localizations=get_localized_name("marriage_config_month_loveroom_price"),
                                  description_localizations=get_localized_description(
                                      "marriage_config_month_loveroom_price"),
                                  )
    async def __marriage_config_month_loveroom_price(self, interaction: Interaction,
                                                     month_loveroom_price: Optional[int] = SlashOption(required=True)):
        if month_loveroom_price <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    month_loveroom_price,
                )
            )
        update_marriage_config_month_loveroom_price(interaction.guild.id, month_loveroom_price)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"marriage_config_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        currency_symbol = get_guild_currency_symbol(interaction.guild.id)
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"marriage_config_{interaction.application_command.name}",
                f"{message} **{month_loveroom_price}** {currency_symbol}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @__marriage_config.subcommand(name="loveroom_category",
                                  name_localizations=get_localized_name("marriage_config_loveroom_category"),
                                  description_localizations=get_localized_description(
                                      "marriage_config_loveroom_category"),
                                  )
    async def __marriage_config_loveroom_category(self, interaction: Interaction,
                                                  loveroom_category: Optional[GuildChannel] = SlashOption(
                                                      required=True)):
        if not isinstance(loveroom_category, nextcord.CategoryChannel):
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    loveroom_category,
                )
            )
        update_marriage_config_loveroom_category(interaction.guild.id, loveroom_category.id)
        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"marriage_config_{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"marriage_config_{interaction.application_command.name}",
                f"{message} {loveroom_category.mention}",
                f"{requested} {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )

    @nextcord.slash_command(name="loveroom_create")
    async def __loveroom_create(self, interaction: Interaction):
        if is_married(interaction.guild.id, interaction.user.id) is False:
            return await interaction.response.send_message(
                embed=construct_error_not_married_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_married_error"
                    ),
                    self.client.user.avatar.url,
                )
            )
        pair_id = get_user_pair_id(interaction.guild.id, interaction.user.id)
        pair = await interaction.guild.fetch_member(pair_id)
        loverooms_state = get_marriage_config_enable_loverooms(interaction.guild.id)
        print(loverooms_state)
        if loverooms_state:
            return await interaction.response.send_message(
                embed=construct_error_not_married_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "loveroom_existing"),
                    self.client.user.avatar.url
                )
            )
        loveroom_category = nextcord.utils.get(interaction.guild.channels,
                                               id=get_marriage_config_loveroom_category(interaction.guild.id))
        loveroom_price = get_marriage_config_month_loveroom_price(interaction.guild.id)
        bal = get_family_money(interaction.guild.id, interaction.user.id)
        if bal < loveroom_price:
            return await interaction.response.send_message(
                embed=construct_error_not_married_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, "on_loveroom_money_error"),
                    self.client.user.avatar.url,
            ))
        update_couple_family_money(interaction.guild.id, interaction.user.id, pair_id, -loveroom_price)
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(
                connect=False,
            ),
            interaction.user: nextcord.PermissionOverwrite(
                connect=True, speak=True, deafen_members=True, priority_speaker=True,
                view_channel=True, manage_channels=True, mute_members=True, move_members=True, stream=True,
            ),
            pair: nextcord.PermissionOverwrite(
                connect=True, speak=True, deafen_members=True, priority_speaker=True,
                view_channel=True, manage_channels=True, mute_members=True, move_members=True, stream=True,
            )
        }
        loveroom = await interaction.guild.create_voice_channel(category=loveroom_category,
                                                                name=f"{interaction.user.name} 🤍 {pair.name}",
                                                                user_limit=2,
                                                                overwrites=overwrites)
        update_user_loveroom_id(interaction.guild.id, interaction.user.id, loveroom.id)
        update_user_loveroom_id(interaction.guild.id, pair_id, loveroom.id)

        message = get_msg_from_locale_by_key(
            interaction.guild.id, f"{interaction.application_command.name}"
        )
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        on_family_balance = get_msg_from_locale_by_key(
            interaction.guild.id, f"on_family_balance"
        )
        family_balance = get_family_money(interaction.guild.id, interaction.user.id)
        await interaction.response.send_message(
            embed=construct_basic_embed(
                f"{interaction.application_command.name}",
                f"{loveroom.mention} {message}",
                f"{requested} {interaction.user}\n{on_family_balance} {family_balance}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        )


def setup(client):
    client.add_cog(Marriage(client))
