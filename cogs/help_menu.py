import nextcord
from nextcord import Interaction, SlashOption, Permissions
from nextcord.ext import commands
from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_keys_value_in_locale,
    get_localized_description,
    get_localized_name,
    localize_name,
    get_guild_locale,
)
from core.embeds import construct_basic_embed, construct_long_embed, DEFAULT_BOT_COLOR
from typing import Optional
from core.emojify import PAPER
import cooldowns


class HelpSelectMenuENG(nextcord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [
            nextcord.SelectOption(
                label="Information",
                description="Help menu 'Information' section",
                emoji="📝",
            ),
            nextcord.SelectOption(
                label="Moderation",
                description="Help menu 'Moderation' section",
                emoji="🛡️",
            ),
            nextcord.SelectOption(
                label="AutoModeration",
                description="Help menu 'AutoModeration' section",
                emoji="🗡️",
            ),
            nextcord.SelectOption(
                label="Economics",
                description="Help menu 'Economics' section",
                emoji="💸",
            ),
            nextcord.SelectOption(
                label="Leveling",
                description="Help menu 'Leveling' section",
                emoji="🐉",
            ),
            nextcord.SelectOption(
                label="Love and marriage",
                description="Help menu 'Love and Marriage' section",
                emoji="🤍",
            ),
            nextcord.SelectOption(
                label="Welcomers and Goodbyes",
                description="Help menu 'Welcomers and Goodbyes' section",
                emoji="👋",
            ),
            nextcord.SelectOption(
                label="Thanks for Nitro Boost",
                description="Help menu 'Thanks for Nitro Boost' section",
                emoji="💎",
            ),
            nextcord.SelectOption(
                label="Emotions, Reactions",
                description="Help menu 'Emotions, Reactions' section",
                emoji="😊",
            ),
            nextcord.SelectOption(
                label="Tickets",
                description="Help menu 'Tickets' section",
                emoji="🎟️",
            ),
            nextcord.SelectOption(
                label="Logs, events logging",
                description="Help menu 'Logs' section",
                emoji="📄",
            ),
            nextcord.SelectOption(
                label="Leaderboards",
                description="Help menu 'Leaderboards' section",
                emoji="🏆",
            ),
            nextcord.SelectOption(
                label="Localisations",
                description="Help menu 'Localisations' section",
                emoji="📙",
            ),
            nextcord.SelectOption(
                label="Profiles",
                description="Help menu 'Profiles' section",
                emoji="👤",
            ),
            nextcord.SelectOption(
                label="Statistics",
                description="Help menu 'Statistics' section",
                emoji="📈",
            ),
            nextcord.SelectOption(
                label="Autoroles",
                description="Help menu 'Autoroles' section",
                emoji="⚙️",
            ),
            nextcord.SelectOption(
                label="Funny",
                description="Help menu 'Autoroles' section",
                emoji="😊",
            ),
        ]
        super().__init__(
            placeholder="Choose section commands you want to view",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "Information":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="📝 Information",
                description="`/help` — Sending help menu\n`/ping` — Bot's latency at this moment\n"
                "`/server` — Information about server\n"
                "`/user` — Information about user or bot",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006554287620497519/ezgif-3-78b49f7c4f"
                ".gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Moderation":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🛡️ Moderation",
                description="`/mute` — Temporarily limit chat to user\n`/unmute` — Remove chat limitation from user\n"
                "`/clear` — Delete messages in channel\n`/warn` — Give warn to user\n"
                "`/unwarn` — Remove warn from user\n`/warns` — List all user warns\n"
                "`/edit_warn` — Edit indicated warn",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006553773235253248/Aduare-artist"
                "-Ayaka-Genshin-Impact-Genshin-Impact-7211646-min.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "AutoModeration":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🗡 Automoderation",
                description="`/automod setup` — Setup full automod system on your server."
                "Works only for community servers with **community** moderation type. "
                "\n`/automod word_add` — Add new forbidden word\n "
                "`/automod word_remove` — Remove word from automod\n`/automod exempt_role_add` — "
                "Works only for community servers with **community** moderation type. Add "
                "exempt role, users with this role can violate automod rules. "
                "\n`/automod exempt_role_remove` — Remove exempt role\n"
                "`/automod exempt_channel_add` — Works only for community servers with **community** "
                "moderation type. "
                "Add exempt channel, users in this channel can violate automod rules "
                "\n`/automod exempt_channel_remove` — Remove exempt channel\n "
                "`/automod nickname_detect` — Turn on/Turn off detection of forbidden words in nicknames\n"
                "`/automod description_detect` — Turn on/Turn off detection of forbidden words in "
                "activity status "
                "активности\n "
                "`/automod link_detect` — Turn on/Turn off link block\n"
                "`/automod enable` — Turn on/Turn off Automoderation system\n"
                "`/automod moderation_mode` — Change moderation type on your server",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1012636048041451540/3.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Economics":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="💸 Economics",
                description="`/timely` — get money timely amount\n`/balance` — Send balance\n`/add_money` — Add money "
                "on someones balance\n "
                "`/remove_money` — Remove money from balance\n`/reset balance` — Reset user balance\n"
                "`/give` — Give money to someone\n`/add-shop` — Add role to shop\n"
                "`/remove-shop` — Remove role from shop\n`/shop` — Server role market\n"
                "`/set currency` — Set new currency symbol\n`/set start_balance` — Set new starting "
                "balance\n`/set timely_amount` — Set timely amount /timely\n`/slots` — Play slots\n"
                "`/blackjack` — Play blackjack\n`/gamble` — Play gamble\n`/wheel` — Spin wheel\n"
                "`/duel` — Start duel\n`/income channel` — Turn on/off income in channel\n"
                "`/income min_max_message` — Set income for message writing\n"
                "`/income min_max_voice` — Set income for being in voice chat\n"
                "`/income messages_per_income` — Set messages amount for income\n"
                "`/income voice_minutes` — Set voice minutes amount for income\n"
                "`/income role_add` — Add income to role per 12 hours\n"
                "`/income role_remove` — Remove role from income system",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006552600377839696/2623939ce6b6b5d3.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Leveling":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🐉 Leveling",
                description="`/level` — Send level card\n`/add_exp` — Add experience\n"
                "`/remove_exp` — Take experience\n`/reset_level` — Reset level and experience\n"
                "`/set level` — Set level to user\n`/set min_max_exp` — Set minimal and maximal "
                "experience gain\n "
                "`/set level_up_messages` — Turn on/off messages about level up",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006597709660172419/1.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Love and marriage":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🤍 Love and marriage",
                description="`/marry` — Send marriage request\n`/loveprofile` — Couple profile\n"
                "`/lovedescription` — Set new description to couple profile\n`/lovedeposit` — Put money "
                "in family bank\n "
                "`/divorce` — Divorce\n`/waifu` — Waifu profile\n"
                "`/like` — Set user you like",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006598206966202368/Aduare-Pixel-Gif"
                "-Pixel-Art-crusaders-quest-6050023.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Welcomers and Goodbyes":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="👋 Welcomers and Goodbyes",
                description="`/set welcome_channel` — Set welcome messages channel\n`/set welcome_message_type` — "
                "Set welcome messages type\n"
                "`/set welcome_message_state` — Turn on/off welcome messages\n`/set welcome_embed` — "
                "Change welcome embed message\n"
                "`/set goodbye_channel` — Set goodbye messages channel\n`/set goodbye_message_type` — "
                "Set goodbye messages type\n"
                "/set goodbye_message_state — Turn on/off goodbye messages\n/set goodbye_embed — "
                "Change goodbye embed message",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006598165358710784/Aduare-Pixel-Gif"
                "-Pixel-Art--6117807.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Emotions, Reactions":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="👋 Emotions",
                description="`/emotion kiss` — Kiss user\n`/emotion hug` — Give a hug to user\n"
                "`/emotion idk` — I dont know\n`/emotion f` — Press F to pay respects\n"
                "`/emotion punch` — Punch user\n`/emotion cry` — Start crying\n"
                "`/emotion bite` — Bite user\n`/emotion spank` — Spank user\n"
                "`/emotion highfive` — Give a high-five to user\n`/emotion pat` — Pat user\n"
                "`/emotion lick` — Lick user",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006553773793083452/Aduare-artist"
                "-Ganyu-Genshin-Impact-Genshin-Impact-7095755-min.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Leaderboards":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🏆 Leaderboards",
                description="`/leaderboard money` — Money leaderboard\n`/leaderboard level` — Levels leaderboard\n"
                "`/leaderboard waifu` — Leaderboard by your waifu price\n"
                "`/leaderboard messages` — Leaderboard by messages count\n"
                "`/leaderboard voice` — Leaderboard by spent time in voice channels",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006605404517716111/aduare-5star.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Profiles":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="👤 Profiles",
                description="`/profile show` — Show profile card\n"
                "`/profile description` — Set profile description\n"
                "`/profile badges` — Show achievements of badges on your profile",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006604685257482373/yae-miko-onsen_1.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Thanks for Nitro Boost":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="💎 Thanks for Nitro Boost",
                description="`/set nitro_channel` — Set channel to send respect and thanks on nitro boost\n`/set nitro_embed` "
                "— Edit on nitro message\n "
                "`/set nitro_messages_state` — Turn on or turn off nitro boost messages",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006607576181506048/Aduare-artist"
                "-Pixel-Gif-Pixel-Art-6691638.gif "
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Tickets":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🎟️ Tickets",
                description="`/setup_tickets` — Setup tickets\n`/set ticket_category` — "
                "Set category channel for tickets\n/set ticket_archive — Set archive category for "
                "tickets\n "
                "`/set ticket_support` — Set role for ticket moderator",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006598165878820979/Aduare-artist"
                "-Pixel-Gif-Pixel-Art-6151675.gif "
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Logs, events logging":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="📄 Logs, events logging",
                description="`/set logging_channel` — Set logging channel\n"
                "`/set logging_state` — Turn on/off logging on your server",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006608424043298836/ezgif-4-ac0c7ef452.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Statistics":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="📈 Statistics",
                description="`/online` — Check your online in voice channels\n"
                "`/messages_counter` — Check your message counter",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006609404428308560/swire-arknights.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Localisations":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="📙 Localisations",
                description="`/set locale` — Set new answer language",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006610072861937744/Aduare-Pixel-Gif"
                "-Pixel-Art-Last-Origin-6066260.gif "
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Autoroles":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="⚙️ Autoroles",
                description="`/autorole on_enter` — Set new autorole on server enter\n`/autorole enable` — "
                "Turn on/off autoroles system\n`/autorole add_for_level` — Add autorole for level\n"
                "`/autorole remove_for_level` — Remove autorole for level\n"
                "`/autorole display_for_level` — Show all autoroles for level\n"
                "`/autorole add_on_reaction` — Add autorole for reaction on message\n"
                "`/autorole remove_on_reaction` — Remove autorole for reaction on message\n"
                "`/autorole display_on_reaction` — Show all autoroles for reaction on message",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006610055589793862/Genshin-Impact-Ero"
                "-Genshin-Impact--Hu-Tao-Genshin-Impact-6593150.gif "
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Funny":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="😊 Funny",
                description="`/brick_knife_evidence_yandere` — Game: Brick Knife Evidence Yandere Tentacles \n"
                "`/ball` — 8ball\n"
                "`/coin` — Flip coin\n"
                "`/cat` — Random cat image\n"
                "`/dog` — Random dog image\n"
                "`/fox` — Random fox image\n"
                "`/bird` — Random birb image\n"
                "`/panda` — Random panda image\n"
                "`/red_panda` — Random red panda image\n",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1011291356267810907/2.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


class HelpSelectMenuRU(nextcord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [
            nextcord.SelectOption(
                label="Информация",
                description="Меню помощи по разделу 'информация'",
                emoji="📝",
            ),
            nextcord.SelectOption(
                label="Модерация",
                description="Меню помощи по разделу 'Модерация'",
                emoji="🛡️",
            ),
            nextcord.SelectOption(
                label="Автомодерация",
                description="Help menu 'Автомодерация' section",
                emoji="🗡️",
            ),
            nextcord.SelectOption(
                label="Экономика",
                description="Меню помощи по разделу 'Экономика'",
                emoji="💸",
            ),
            nextcord.SelectOption(
                label="Уровни",
                description="Меню помощи по разделу 'Уровни'",
                emoji="🐉",
            ),
            nextcord.SelectOption(
                label="Любовь и свадьбы",
                description="Меню помощи по разделу 'Любовь и свадьбы'",
                emoji="🤍",
            ),
            nextcord.SelectOption(
                label="Приветствия и прощания",
                description="Меню помощи по разделу 'Приветствия и прощания'",
                emoji="👋",
            ),
            nextcord.SelectOption(
                label="Благодарности за нитро буст(alpha)",
                description="Меню помощи по разделу 'Нитро'",
                emoji="💎",
            ),
            nextcord.SelectOption(
                label="Эмоции, Реакции",
                description="Меню помощи по разделу 'Эмоции, Реакции'",
                emoji="😊",
            ),
            nextcord.SelectOption(
                label="Тикеты",
                description="Меню помощи по разделу 'Тикеты'",
                emoji="🎟️",
            ),
            nextcord.SelectOption(
                label="Логи, Логирование событий",
                description="Меню помощи по разделу 'Логи'",
                emoji="📄",
            ),
            nextcord.SelectOption(
                label="Топы", description="Меню помощи по разделу 'Топы'", emoji="🏆"
            ),
            nextcord.SelectOption(
                label="Локализации",
                description="Меню помощи по разделу 'Локализации'",
                emoji="📙",
            ),
            nextcord.SelectOption(
                label="Профили",
                description="Меню помощи по разделу 'Профили'",
                emoji="👤",
            ),
            nextcord.SelectOption(
                label="Статистика",
                description="Меню помощи по разделу 'Статистика'",
                emoji="📈",
            ),
            nextcord.SelectOption(
                label="Автороли",
                description="Меню помощи по разделу 'Автороли'",
                emoji="⚙️",
            ),
            nextcord.SelectOption(
                label="Развлечения",
                description="Меню помощи по разделу 'Развлечения'",
                emoji="😊",
            ),
        ]
        super().__init__(
            placeholder="Выберите раздел, команды которого вы хотите увидеть",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "Информация":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="📝 Информация",
                description="`/help` — Отправляет меню команд\n`/ping` — Задержка бота в данный момент\n"
                "`/server` — Информация о сервере\n"
                "`/user` — Информация о пользователе",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006554287620497519/ezgif-3-78b49f7c4f"
                ".gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Модерация":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🛡️ Модерация",
                description="`/mute` — Временно ограничить чат пользователю\n`/unmute` — Снять ограничение чата\n"
                "`/clear` — Удаляет сообщения\n`/warn` — Выдать предупреждение\n"
                "`/unwarn` — Снять предупреждение\n`/warns` — Список предупреждений пользователя\n"
                "`/edit_warn` — Изменить предупреждение",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006553773235253248/Aduare-artist"
                "-Ayaka-Genshin-Impact-Genshin-Impact-7211646-min.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Автомодерация":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🗡 Автомодерация",
                description="`/automod setup` — Устанавливает полную систему автомодерации без ограничений на "
                "сервере. Работает только для серверов - сообществ с **community** типом "
                "модерации\n`/automod word_add` — Добавляет новое запрещённое слово для автомодерации\n "
                "`/automod word_remove` — Удаляет слово из автомодерации\n`/automod exempt_role_add` — "
                "Работает только для серверов - сообществ с **community** типом модерации. Добавляет "
                "исключение для данной роли, пользователям с этой ролью можно будет нарушать правила "
                "автомодерации.\n`/automod exempt_role_remove` — Убирает исключение для данной роли\n"
                "`/automod exempt_channel_add` — Работает только для серверов - сообществ с **community** "
                "типом модерации. Добавляет исключение для данного канала, в нём можно будет нарушать "
                "правила автомодерации\n`/automod exempt_channel_remove` — Убирает исключение для канала\n "
                "`/automod nickname_detect` — Включает/Отключает поиск запрещённых слов в никнеймах\n"
                "`/automod description_detect` — Включает/Отключает поиск запрещённых слов в статусах "
                "активности\n "
                "`/automod link_detect` — Включает/Отключает блокировку ссылок\n"
                "`/automod enable` — Включает/Отключает автомодерацию\n"
                "`/automod moderation_mode` — Изменяет вид модерации на сервере",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1012636048041451540/3.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Экономика":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="💸 Экономика",
                description="`/timely` — получить денежную выплату\n`/balance` — Узнать баланс\n`/add_money` — "
                "Добавить деньги\n "
                "`/remove_money` — Забрать деньги\n`/reset balance` — Сбросить баланс\n"
                "`/give` — Передать валюту\n`/add-shop` — Добавить роль в магазин\n"
                "`/remove-shop` — Убрать роль из магазина\n`/shop` — Магазин сервера\n"
                "`/set currency` — Установить символ валюты\n`/set start_balance` — Установить начальный "
                "баланс\n`/set timely_amount` — Установить выплату /timely\n`/slots` — Сыграть в слоты\n"
                "`/blackjack` — Сыграть в блэкджек\n`/gamble` — Сыграть в броски\n`/wheel` — Крутить колесо\n"
                "`/duel` — Начать дуэль\n`/income channel` — Отключить/Включить доход в канале\n"
                "`/income min_max_message` — Настроить доход за написание сообщений\n"
                "`/income min_max_voice` — Настроить доход за пребывание в голосовом чате\n"
                "`/income messages_per_income` — Настроить кол-во сообщений для выдачи дохода\n"
                "`/income voice_minutes` — Настроить кол-во минут в голосовом чате для выдачи дохода\n"
                "`/income role_add` — Добавить выдачу раз в 12 часов валюты роли\n"
                "`/income role_remove` — Убрать выдачу раз в 12 часов валюты роли",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006552600377839696/2623939ce6b6b5d3.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Уровни":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🐉 Уровни",
                description="`/level` — Узнать уровень\n`/add_exp` — Добавить опыт\n"
                "`/remove_exp` — Забрать опыт\n`/reset_level` — Сбросить уровень и опыт\n"
                "`/set level` — Установить уровень\n`/set min_max_exp` — Установить промежуток опыта\n"
                "`/set level_up_messages` — Вкл/выкл сообщения о повышении уровня",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006597709660172419/1.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Любовь и свадьбы":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🤍 Любовь и свадьбы",
                description="`/marry` — Отправить запрос на свадьбу\n`/loveprofile` — Профиль пары\n"
                "`/lovedescription` — Описание профиля пары\n`/lovedeposit` — Положить деньги на семейный "
                "счёт\n "
                "`/divorce` — Развод\n`/waifu` — Профиль вайфу\n"
                "`/like` — Указать пользователя который нравится",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006598206966202368/Aduare-Pixel-Gif"
                "-Pixel-Art-crusaders-quest-6050023.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Приветствия и прощания":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="👋 Приветствия и прощания",
                description="`/set welcome_channel` — Установить канал приветствий\n`/set welcome_message_type` — "
                "Установить тип приветствий\n"
                "`/set welcome_message_state` — Включить/отключить приветствия\n`/set welcome_embed` — "
                "Настроить приветственный эмбед\n"
                "`/set goodbye_channel` — Установить канал прощаний\n`/set goodbye_message_type` — "
                "Установить тип прощаний\n"
                "`/set goodbye_message_state` — Включить/отключить приветствия\n`/set goodbye_embed` — "
                "Настроить прощальный эмбед",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006598165358710784/Aduare-Pixel-Gif"
                "-Pixel-Art--6117807.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Эмоции, Реакции":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="👋 Эмоции",
                description="`/emotion kiss` — Поцеловать пользователя\n`/emotion hug` — Обнять пользователя\n"
                "`/emotion idk` — Не знаю\n`/emotion f` — Press F to pay respects\n"
                "`/emotion punch` — Ударить пользователя\n`/emotion cry` — Заплакать\n"
                "`/emotion bite` — Укусить пользователя\n`/emotion spank` — Отшлёпать пользователя\n"
                "`/emotion highfive` — Дать пять пользователю\n`/emotion pat` — Погладить пользователя\n"
                "`/emotion lick` — Лизнуть пользователя",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006553773793083452/Aduare-artist"
                "-Ganyu-Genshin-Impact-Genshin-Impact-7095755-min.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Топы":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🏆 Топы",
                description="`/leaderboard money` — Топ по деньгам\n`/leaderboard level` — Топ по уровням\n"
                "`/leaderboard waifu` — Топ по общей стоимости вайфу(подаренных подарков)\n"
                "`/leaderboard messages` — Топ по количеству сообщений\n"
                "`/leaderboard voice` — Топ по времени в голосовых каналах",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006605404517716111/aduare-5star.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Профили":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="👤 Профили",
                description="`/profile show` — Профиль\n"
                "`/profile description` — Установить описание профиля\n"
                "/`profile badges` — Отобразить достижения значков профиля",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006604685257482373/yae-miko-onsen_1.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Благодарности за нитро буст(alpha)":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="💎 Благодарности за нитро буст(alpha)",
                description="`/set nitro_channel` — Установить канал Благодарности за нитро буст\n`/set nitro_embed` "
                "— Установить нитро сообщение\n "
                "`/set nitro_messages_state` — Включить/отключить благодарности за буст",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006607576181506048/Aduare-artist"
                "-Pixel-Gif-Pixel-Art-6691638.gif "
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Тикеты":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="🎟️ Тикеты",
                description="`/setup_tickets` — Установить каналы и категории тикетов\n`/set ticket_category` — "
                "Установить категорию для тикетов\n/set ticket_archive — Установить категорию - архив для "
                "тикетов\n "
                "`/set ticket_support` — Установить роль модератора тикетов",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006598165878820979/Aduare-artist"
                "-Pixel-Gif-Pixel-Art-6151675.gif "
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Логи, Логирование событий":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="📄 Логи, Логирование событий",
                description="`/set logging_channel` — Установить канал для логов\n"
                "`/set logging_state` — Включить/выключить логирование",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006608424043298836/ezgif-4-ac0c7ef452.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Статистика":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="📈 Статистика",
                description="`/online` — Посмотреть онлайн в голосовых\n"
                "`/messages_counter` — Узнать количество сообщений",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006609404428308560/swire-arknights.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Локализации":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="📙 Локализации",
                description="`/set locale` — Установить язык ответа",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006610072861937744/Aduare-Pixel-Gif"
                "-Pixel-Art-Last-Origin-6066260.gif "
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Автороли":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="⚙️ Автороли",
                description="`/autorole on_enter` — Установить автороль на входе\n`/autorole enable` — "
                "Включает/выключает автороли\n`/autorole add_for_level` — Добавить автороль за уровень\n"
                "`/autorole remove_for_level` — Убрать автороль за уровень\n"
                "`/autorole display_for_level` — Показать все автороли за уровень\n"
                "`/autorole add_on_reaction` — Добавить автороль за реакцию на сообщение\n"
                "`/autorole remove_on_reaction` — Убрать автороль за реакцию на сообщение\n"
                "`/autorole display_on_reaction` — Показать все автороли за реакции на сообщение",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006610055589793862/Genshin-Impact-Ero"
                "-Genshin-Impact--Hu-Tao-Genshin-Impact-6593150.gif "
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Развлечения":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="😊 Развлечения",
                description="`/brick_knife_evidence_yandere` — Игра: Кирпич Нож Компромат Яндере Тентакли \n"
                "`/ball` — Шар предсказаний\n"
                "`/coin` — Подбросить монетку\n"
                "`/cat` — Случайное изображение котика\n"
                "`/dog` — Случайное изображение собаки\n"
                "`/fox` — Случайное изображение лисы\n"
                "`/bird` — Случайное изображение птички\n"
                "`/panda` — Случайное изображение панды\n"
                "`/red_panda` — Случайное изображение красной панды\n",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1011291356267810907/2.gif"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


class HelpMenuView(nextcord.ui.View):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        super().__init__()

        guild_locale = get_guild_locale(guild_id)
        if guild_locale == "ru_ru":
            self.add_item(HelpSelectMenuRU())
        else:
            self.add_item(HelpSelectMenuENG())


class HelpMenu(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="help",
        description="Shows help menu",
        name_localizations=get_localized_name("help"),
        description_localizations=get_localized_description("help"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __help(self, interaction: Interaction):
        embed = nextcord.Embed(
            color=DEFAULT_BOT_COLOR,
            title=f"{PAPER} {localize_name(interaction.guild.id, interaction.application_command.name).capitalize()}",
            description=get_msg_from_locale_by_key(interaction.guild.id, "help"),
        )
        view = HelpMenuView(interaction.guild.id)
        embed.set_image(url="https://c.tenor.com/K0hCHT6qFbMAAAAd/mobius-pixel-art.gif")
        await interaction.response.send_message(embed=embed, view=view)


def setup(client):
    client.add_cog(HelpMenu(client))
