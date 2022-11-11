import random
import sqlite3

import nextcord

from core.clan.getters import (
    get_clan_max_attack,
    get_clan_min_attack,
    get_clan_level,
    get_clan_exp,
    get_clan_storage,
    get_clan_guild_boss_hp,
    get_clan_guild_boss_level,
    get_clan_boss_hp_limit,
    get_server_clan_change_image_cost,
    get_server_clan_upgrade_boss_cost,
    get_server_clan_upgrade_attack_cost,
    get_server_clan_change_icon_cost,
    get_server_clan_upgrade_limit_cost,
    get_server_clan_create_cost,
    get_upgrade_limit_multiplier,
    get_boss_upgrade_multiplier,
    get_clan_member_limit,
    get_user_clan_id,
    get_server_clan_change_color_cost
)
from core.locales.getters import get_msg_from_locale_by_key, localize_name
from core.emojify import SHOP
from core.embeds import DEFAULT_BOT_COLOR

from core.clan.storage import boss_rewards


# Clan update


def update_clan_icon(guild_id: int, clan_id: int, icon_url: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET icon = ? WHERE guild_id = ? AND clan_id = ?"
    values = (icon_url, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_min_attack(guild_id: int, clan_id: int, min_attack_to_add: int) -> None:
    min_attack_now = get_clan_min_attack(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET min_attack = ? WHERE guild_id = ? AND clan_id = ?"
    values = (min_attack_now + min_attack_to_add, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_max_attack(guild_id: int, clan_id: int, max_attack_to_add: int) -> None:
    max_attack_now = get_clan_max_attack(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET max_attack = ? WHERE guild_id = ? AND clan_id = ?"
    values = (max_attack_now + max_attack_to_add, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_level(guild_id: int, clan_id: int, levels_to_add: int) -> None:
    clan_level = get_clan_level(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_level = ? WHERE guild_id = ? AND clan_id = ?"
    values = (clan_level + levels_to_add, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_exp(guild_id: int, clan_id: int, exp_to_add: int) -> None:
    clan_exp = get_clan_exp(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_exp = ? WHERE guild_id = ? AND clan_id = ?"
    values = (clan_exp + exp_to_add, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_storage(guild_id: int, clan_id: int, money: int) -> None:
    storage = get_clan_storage(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET storage = ? WHERE guild_id = ? AND clan_id = ?"
    values = (storage + money, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_description(guild_id: int, clan_id: int, description: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_description = ? WHERE guild_id = ? AND clan_id = ?"
    values = (description, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_boss_level(guild_id: int, clan_id: int, levels_to_update: int) -> None:
    guild_boss_level = get_clan_guild_boss_level(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET guild_boss_level = ? WHERE guild_id = ? AND clan_id = ?"
    values = (guild_boss_level + levels_to_update, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_boss_hp(guild_id: int, clan_id: int, hp_to_update: int) -> None:
    guild_boss_hp = get_clan_guild_boss_hp(guild_id, clan_id)
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET guild_boss_hp = ? WHERE guild_id = ? AND clan_id = ?"
    values = (guild_boss_hp + hp_to_update, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def set_clan_boss_hp(guild_id: int, clan_id: int, hp_to_set: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET guild_boss_hp = ? WHERE guild_id = ? AND clan_id = ?"
    values = (hp_to_set, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_image(guild_id: int, clan_id: int, image: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET image = ? WHERE guild_id = ? AND clan_id = ?"
    values = (image, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_owner_id(guild_id: int, clan_id: int, owner_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET owner_id = ? WHERE guild_id = ? AND clan_id = ?"
    values = (owner_id, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_name(guild_id: int, owner_id: int, name: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_name = ? WHERE guild_id = ? AND owner_id = ?"
    values = (name, guild_id, owner_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_desc_on_creation(guild_id: int, owner_id: int, desc: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_description = ? WHERE guild_id = ? AND owner_id = ?"
    values = (desc, guild_id, owner_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_color(guild_id: int, owner_id: int, color: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET clan_color = ? WHERE guild_id = ? AND owner_id = ?"
    values = (color, guild_id, owner_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_icon_on_creation(guild_id: int, owner_id: int, icon: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET icon = ? WHERE guild_id = ? AND owner_id = ?"
    values = (icon, guild_id, owner_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_clan_member_limit(
    guild_id: int, clan_id: int, new_member_limit: int
) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clans SET member_limit = ? WHERE guild_id = ? AND clan_id = ?"
    values = (new_member_limit, guild_id, clan_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_clan_id(guild_id: int, user_id: int, clan_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_members SET clan_id = ? WHERE guild_id = ? AND user_id = ?"
    values = (clan_id, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_user_join_date(guild_id: int, user_id: int, join_date: str) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_members SET join_date = ? WHERE guild_id = ? AND user_id = ?"
    values = (join_date, guild_id, user_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


# Config update


def update_server_clan_create_cost(guild_id: int, clan_creation_cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET create_cost = ? WHERE guild_id = ?"
    values = (clan_creation_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_upgrade_attack_cost(
    guild_id: int, upgrade_attack_cost: int
) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET upgrade_attack_cost = ? WHERE guild_id = ?"
    values = (upgrade_attack_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_upgrade_limit_cost(
    guild_id: int, upgrade_limit_cost: int
) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET upgrade_limit_cost = ? WHERE guild_id = ?"
    values = (upgrade_limit_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_change_icon_cost(guild_id: int, change_icon_cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET change_icon_cost = ? WHERE guild_id = ?"
    values = (change_icon_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_change_image_cost(guild_id: int, change_image_cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET change_icon_cost = ? WHERE guild_id = ?"
    values = (change_image_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_upgrade_boss_cost(guild_id: int, upgrade_boss_cost: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET upgrade_boss_cost = ? WHERE guild_id = ?"
    values = (upgrade_boss_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_create_clan_channels(
    guild_id: int, create_clan_channels: bool
) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET create_clan_channels = ? WHERE guild_id = ?"
    values = (create_clan_channels, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_change_color_cost(
    guild_id: int, change_color_cost: int
) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET change_color_cost = ? WHERE guild_id = ?"
    values = (change_color_cost, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def update_server_clan_voice_category(
    guild_id: int, clan_voice_category: int
) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "UPDATE clan_config SET clan_voice_category = ? WHERE guild_id = ?"
    values = (clan_voice_category, guild_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def delete_clan(guild_id: int, owner_id: int) -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    sql = "DELETE from clans WHERE guild_id = ? AND owner_id = ?"
    values = (guild_id, owner_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return


def accomplish_boss_rewards(guild_id: int, clan_id: int) -> tuple[int, int]:
    boss_level = get_clan_guild_boss_level(guild_id, clan_id)
    money_reward = random.randint(
        boss_rewards[boss_level]["money"]["min"],
        boss_rewards[boss_level]["money"]["max"],
    )
    exp_reward = random.randint(
        boss_rewards[boss_level]["exp"]["min"], boss_rewards[boss_level]["exp"]["max"]
    )
    update_clan_storage(guild_id, clan_id, money_reward)
    update_clan_exp(guild_id, clan_id, exp_reward)
    return money_reward, exp_reward


def resurrect_boss(guild_id: int, clan_id: int) -> None:
    hp_limit = get_clan_boss_hp_limit(guild_id, clan_id)
    set_clan_boss_hp(guild_id, clan_id, hp_limit)
    return


def clan_level_up(guild_id, clan_id):
    clan_exp = get_clan_exp(guild_id, clan_id)
    clan_level = get_clan_level(guild_id, clan_id)
    leveling_formula = round((17 * (clan_level**3)) + 11)
    if clan_exp >= leveling_formula:
        return True
    else:
        return False


def calculate_level(guild_id: int, clan_id: int):
    clan_exp = get_clan_exp(guild_id, clan_id)
    clan_level = get_clan_level(guild_id, clan_id)
    if clan_exp > 0:
        leveling_formula = round((17 * (clan_level**3)) + 11)
        while clan_level_up(guild_id, clan_id):
            update_clan_exp(guild_id, clan_id, -leveling_formula)
            update_clan_level(guild_id, clan_id, 1)
            clan_level = get_clan_level(guild_id, clan_id)
            leveling_formula = round((17 * (clan_level**3)) + 11)


def redraw_shop_embed(interaction: nextcord.Interaction) -> nextcord.Embed:
    embed = nextcord.Embed(
        color=DEFAULT_BOT_COLOR,
        title=f"{SHOP} {localize_name(interaction.guild.id, 'clan_shop').capitalize()}",
    )
    embed.add_field(name="```#.  ```", value="```1. ```", inline=True)
    embed.add_field(
        name="```                 Имя Товара                 ```",
        value=f"```{get_msg_from_locale_by_key(interaction.guild.id, 'clan_shop_1')}```",
        inline=True,
    )
    embed.add_field(
        name=f"```   {get_msg_from_locale_by_key(interaction.guild.id, 'price')}   ```",
        value=f"``` {get_server_clan_upgrade_limit_cost(interaction.guild.id) * get_upgrade_limit_multiplier(get_clan_member_limit(interaction.guild.id, get_user_clan_id(interaction.guild.id, interaction.user.id)))}```",
        inline=True,
    )
    embed.add_field(name="```#.  ```", value="```2. ```", inline=True)
    embed.add_field(
        name="```                 Имя Товара                 ```",
        value=f"```{get_msg_from_locale_by_key(interaction.guild.id, 'clan_shop_2')}```",
        inline=True,
    )
    embed.add_field(
        name=f"```   {get_msg_from_locale_by_key(interaction.guild.id, 'price')}   ```",
        value=f"``` {get_server_clan_change_image_cost(interaction.guild.id)}```",
        inline=True,
    )
    embed.add_field(name="```#.  ```", value="```3. ```", inline=True)
    embed.add_field(
        name="```                 Имя Товара                 ```",
        value=f"```{get_msg_from_locale_by_key(interaction.guild.id, 'clan_shop_3')}```",
        inline=True,
    )
    embed.add_field(
        name=f"```   {get_msg_from_locale_by_key(interaction.guild.id, 'price')}   ```",
        value=f"``` {get_server_clan_change_icon_cost(interaction.guild.id)}```",
        inline=True,
    )
    embed.add_field(name="```#.  ```", value="```4. ```", inline=True)
    embed.add_field(
        name="```                 Имя Товара                 ```",
        value=f"```{get_msg_from_locale_by_key(interaction.guild.id, 'clan_shop_4')}```",
        inline=True,
    )
    embed.add_field(
        name=f"```   {get_msg_from_locale_by_key(interaction.guild.id, 'price')}   ```",
        value=f"``` {round(get_server_clan_upgrade_attack_cost(interaction.guild.id) + (100/(2/get_clan_min_attack(interaction.guild.id, get_user_clan_id(interaction.guild.id, interaction.user.id))))/100)}```",
        inline=True,
    )
    embed.add_field(name="```#.  ```", value="```5. ```", inline=True)
    embed.add_field(
        name="```                 Имя Товара                 ```",
        value=f"```{get_msg_from_locale_by_key(interaction.guild.id, 'clan_shop_5')}```",
        inline=True,
    )
    embed.add_field(
        name=f"```   {get_msg_from_locale_by_key(interaction.guild.id, 'price')}   ```",
        value=f"``` "
        f"{get_server_clan_upgrade_boss_cost(interaction.guild.id) * get_boss_upgrade_multiplier(get_clan_guild_boss_level(interaction.guild.id, get_user_clan_id(interaction.guild.id, interaction.user.id)))}```",
        inline=True,
    )
    embed.add_field(name="```#.  ```", value="```6. ```", inline=True)
    embed.add_field(
        name="```                 Имя Товара                 ```",
        value=f"```{get_msg_from_locale_by_key(interaction.guild.id, 'clan_shop_6')}```",
        inline=True,
    )
    embed.add_field(
        name=f"```   {get_msg_from_locale_by_key(interaction.guild.id, 'price')}   ```",
        value=f"``` {get_server_clan_change_color_cost(interaction.guild.id)}```",
        inline=True,
    )
    return embed
