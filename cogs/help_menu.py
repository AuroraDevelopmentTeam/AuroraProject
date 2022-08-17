import nextcord
from nextcord import Interaction, SlashOption, Permissions
from nextcord.ext import commands
from core.locales.getters import (
    get_msg_from_locale_by_key,
    get_keys_value_in_locale,
    get_localized_description,
    get_localized_name,
    localize_name,
)
from core.embeds import construct_basic_embed, construct_long_embed, DEFAULT_BOT_COLOR
from typing import Optional
from core.emojify import PAPER
import cooldowns


class HelpSelectMenu(nextcord.ui.Select):
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
        elif self.values[0] == "Экономика":
            embed = nextcord.Embed(
                color=DEFAULT_BOT_COLOR,
                title="💸 Экономика",
                description="`/balance` — Узнать баланс\n`/add_money` — Добавить деньги\n"
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
                "/set goodbye_message_state — Включить/отключить приветствия\n/set goodbye_embed — "
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
                description="`/profile me` — Профиль\n"
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
                description="`/set autorole` — Установить автороль на входе\n`/set autoroles_state` — "
                "Включает/выключает автороли ",
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/772385814483173398/1006610055589793862/Genshin-Impact-Ero"
                "-Genshin-Impact--Hu-Tao-Genshin-Impact-6593150.gif "
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


class HelpMenuView(nextcord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(HelpSelectMenu())


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
            description="Приветствую тебя, **пользователь**\n\nСпасибо за то, что выбрали Аврору как вашего бота. "
            "Это команда для помощи и навигации по моим командам!\n\n**Выбери раздел**, чтобы посмотреть "
            "его команды. \n\n[Сайт бота](https://clonexy700.github.io/AuroraBotWebsite/index.html)\n"
            "[Команды в браузере](https://clonexy700.github.io/AuroraBotWebsite/commands.html)\n"
            "[Нашёл баг? Проблема? Поможем! Сервер поддержки](https://discord.gg/5j9hmZw6yY)",
        )
        view = HelpMenuView()
        embed.set_image(url="https://c.tenor.com/K0hCHT6qFbMAAAAd/mobius-pixel-art.gif")
        await interaction.response.send_message(embed=embed, view=view)


def setup(client):
    client.add_cog(HelpMenu(client))
