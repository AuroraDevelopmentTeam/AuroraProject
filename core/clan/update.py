import random
from core.db_utils import execute_update

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


async def update_clan_icon(guild_id: int, clan_id: int, icon_url: str) -> None:
    sql = "UPDATE clans SET icon = %s WHERE guild_id = %s AND clan_id = %s"
    values = (icon_url, guild_id, clan_id)
    await execute_update(sql, values)


async def update_clan_min_attack(guild_id: int, clan_id: int, min_attack_to_add: int) -> None:
    min_attack_now = await get_clan_min_attack(guild_id, clan_id)
    sql = "UPDATE clans SET min_attack = %s WHERE guild_id = %s AND clan_id = %s"
    values = (min_attack_now + min_attack_to_add, guild_id, clan_id)
    await execute_update(sql, values)


async def update_clan_max_attack(guild_id: int, clan_id: int, max_attack_to_add: int) -> None:
    max_attack_now = await get_clan_max_attack(guild_id, clan_id)
    sql = "UPDATE clans SET max_attack = %s WHERE guild_id = %s AND clan_id = %s"
    values = (max_attack_now + max_attack_to_add, guild_id, clan_id)
    await execute_update(sql, values)


async def update_clan_level(guild_id: int, clan_id: int, levels_to_add: int) -> None:
    clan_level = await get_clan_level(guild_id, clan_id)
    sql = "UPDATE clans SET clan_level = %s WHERE guild_id = %s AND clan_id = %s"
    values = (clan_level + levels_to_add, guild_id, clan_id)
    await execute_update(sql, values)


async def update_clan_exp(guild_id: int, clan_id: int, exp_to_add: int) -> None:
    clan_exp = await get_clan_exp(guild_id, clan_id)
    sql = "UPDATE clans SET clan_exp = %s WHERE guild_id = %s AND clan_id = %s"
    values = (clan_exp + exp_to_add, guild_id, clan_id)
    await execute_update(sql, values)


async def update_clan_storage(guild_id: int, clan_id: int, money: int) -> None:
    storage = await get_clan_storage(guild_id, clan_id)
    sql = "UPDATE clans SET storage = %s WHERE guild_id = %s AND clan_id = %s"
    values = (storage + money, guild_id, clan_id)
    await execute_update(sql, values)


async def update_clan_description(guild_id: int, clan_id: int, description: str) -> None:
    sql = "UPDATE clans SET clan_description = %s WHERE guild_id = %s AND clan_id = %s"
    values = (description, guild_id, clan_id)
    await execute_update(sql, values)


async def update_clan_boss_level(guild_id: int, clan_id: int, levels_to_update: int) -> None:
    guild_boss_level = await get_clan_guild_boss_level(guild_id, clan_id)
    sql = "UPDATE clans SET guild_boss_level = %s WHERE guild_id = %s AND clan_id = %s"
    values = (guild_boss_level + levels_to_update, guild_id, clan_id)
    await execute_update(sql, values)


async def update_clan_boss_hp(guild_id: int, clan_id: int, hp_to_update: int) -> None:
    guild_boss_hp = await get_clan_guild_boss_hp(guild_id, clan_id)
    sql = "UPDATE clans SET guild_boss_hp = %s WHERE guild_id = %s AND clan_id = %s"
    values = (guild_boss_hp + hp_to_update, guild_id, clan_id)
    await execute_update(sql, values)


async def set_clan_boss_hp(guild_id: int, clan_id: int, hp_to_set: int) -> None:
    sql = "UPDATE clans SET guild_boss_hp = %s WHERE guild_id = %s AND clan_id = %s"
    values = (hp_to_set, guild_id, clan_id)
    await (sql, values)


async def update_clan_image(guild_id: int, clan_id: int, image: str) -> None:
    sql = "UPDATE clans SET image = %s WHERE guild_id = %s AND clan_id = %s"
    values = (image, guild_id, clan_id)
    await execute_update(sql, values)


async def update_clan_owner_id(guild_id: int, clan_id: int, owner_id: int) -> None:
    sql = "UPDATE clans SET owner_id = %s WHERE guild_id = %s AND clan_id = %s"
    values = (owner_id, guild_id, clan_id)
    await execute_update(sql, values)


async def update_clan_name(guild_id: int, owner_id: int, name: str) -> None:
    sql = "UPDATE clans SET clan_name = %s WHERE guild_id = %s AND owner_id = %s"
    values = (name, guild_id, owner_id)
    await execute_update(sql, values)


async def update_clan_desc_on_creation(guild_id: int, owner_id: int, desc: str) -> None:
    sql = "UPDATE clans SET clan_description = %s WHERE guild_id = %s AND owner_id = %s"
    values = (desc, guild_id, owner_id)
    await execute_update(sql, values)

async def update_clan_color(guild_id: int, owner_id: int, color: str) -> None:
    sql = "UPDATE clans SET clan_color = %s WHERE guild_id = %s AND owner_id = %s"
    values = (color, guild_id, owner_id)
    await execute_update(sql, values)


async def update_clan_icon_on_creation(guild_id: int, owner_id: int, icon: str) -> None:
    sql = "UPDATE clans SET icon = %s WHERE guild_id = %s AND owner_id = %s"
    values = (icon, guild_id, owner_id)
    await execute_update(sql, values)


async def update_clan_member_limit(
    guild_id: int, clan_id: int, new_member_limit: int
) -> None:
    sql = "UPDATE clans SET member_limit = %s WHERE guild_id = %s AND clan_id = %s"
    values = (new_member_limit, guild_id, clan_id)
    await execute_update(sql, values)


async def update_user_clan_id(guild_id: int, user_id: int, clan_id: int) -> None:
    sql = "UPDATE clan_members SET clan_id = %s WHERE guild_id = %s AND user_id = %s"
    values = (clan_id, guild_id, user_id)
    await execute_update(sql, values)


async def update_user_join_date(guild_id: int, user_id: int, join_date: str) -> None:
    sql = "UPDATE clan_members SET join_date = %s WHERE guild_id = %s AND user_id = %s"
    values = (join_date, guild_id, user_id)
    await execute_update(sql, values)


# Config update


async def update_server_clan_create_cost(guild_id: int, clan_creation_cost: int) -> None:
    sql = "UPDATE clan_config SET create_cost = %s WHERE guild_id = %s"
    values = (clan_creation_cost, guild_id)
    await execute_update(sql, values)


async def update_server_clan_upgrade_attack_cost(
    guild_id: int, upgrade_attack_cost: int
) -> None:
    sql = "UPDATE clan_config SET upgrade_attack_cost = %s WHERE guild_id = %s"
    values = (upgrade_attack_cost, guild_id)
    await execute_update(sql, values)


async def update_server_clan_upgrade_limit_cost(
    guild_id: int, upgrade_limit_cost: int
) -> None:
    sql = "UPDATE clan_config SET upgrade_limit_cost = %s WHERE guild_id = %s"
    values = (upgrade_limit_cost, guild_id)
    await execute_update(sql, values)


async def update_server_clan_change_icon_cost(guild_id: int, change_icon_cost: int) -> None:
    sql = "UPDATE clan_config SET change_icon_cost = %s WHERE guild_id = %s"
    values = (change_icon_cost, guild_id)
    await execute_update(sql, values)


async def update_server_clan_change_image_cost(guild_id: int, change_image_cost: int) -> None:
    sql = "UPDATE clan_config SET change_icon_cost = %s WHERE guild_id = %s"
    values = (change_image_cost, guild_id)
    await execute_update(sql, values)


async def update_server_clan_upgrade_boss_cost(guild_id: int, upgrade_boss_cost: int) -> None:
    sql = "UPDATE clan_config SET upgrade_boss_cost = %s WHERE guild_id = %s"
    values = (upgrade_boss_cost, guild_id)
    await execute_update(sql, values)


async def update_server_create_clan_channels(
    guild_id: int, create_clan_channels: bool
) -> None:
    sql = "UPDATE clan_config SET create_clan_channels = %s WHERE guild_id = %s"
    values = (create_clan_channels, guild_id)
    await execute_update(sql, values)


async def update_server_change_color_cost(
    guild_id: int, change_color_cost: int
) -> None:
    sql = "UPDATE clan_config SET change_color_cost = %s WHERE guild_id = %s"
    values = (change_color_cost, guild_id)
    await execute_update(sql, values)


async def update_server_clan_voice_category(
    guild_id: int, clan_voice_category: int
) -> None:
    sql = "UPDATE clan_config SET clan_voice_category = %s WHERE guild_id = %s"
    values = (clan_voice_category, guild_id)
    await execute_update(sql, values)


async def delete_clan(guild_id: int, owner_id: int) -> None:
    sql = "DELETE from clans WHERE guild_id = %s AND owner_id = %s"
    values = (guild_id, owner_id)
    await execute_update(sql, values)


async def accomplish_boss_rewards(guild_id: int, clan_id: int) -> tuple[int, int]:
    boss_level = await get_clan_guild_boss_level(guild_id, clan_id)
    money_reward = random.randint(
        boss_rewards[boss_level]["money"]["min"],
        boss_rewards[boss_level]["money"]["max"],
    )
    exp_reward = random.randint(
        boss_rewards[boss_level]["exp"]["min"], boss_rewards[boss_level]["exp"]["max"]
    )
    await update_clan_storage(guild_id, clan_id, money_reward)
    await update_clan_exp(guild_id, clan_id, exp_reward)
    return money_reward, exp_reward


async def resurrect_boss(guild_id: int, clan_id: int) -> None:
    hp_limit = await get_clan_boss_hp_limit(guild_id, clan_id)
    await set_clan_boss_hp(guild_id, clan_id, hp_limit)


async def clan_level_up(guild_id, clan_id):
    clan_exp = await get_clan_exp(guild_id, clan_id)
    clan_level = await get_clan_level(guild_id, clan_id)
    leveling_formula = round((17 * (clan_level**3)) + 11)
    if clan_exp >= leveling_formula:
        return True
    return False


async def calculate_level(guild_id: int, clan_id: int):
    clan_exp = await get_clan_exp(guild_id, clan_id)
    clan_level = await get_clan_level(guild_id, clan_id)
    if clan_exp > 0:
        leveling_formula = round((17 * (clan_level**3)) + 11)
        while await clan_level_up(guild_id, clan_id):
            await update_clan_exp(guild_id, clan_id, -leveling_formula)
            await update_clan_level(guild_id, clan_id, 1)
            clan_level = await get_clan_level(guild_id, clan_id)
            leveling_formula = round((17 * (clan_level**3)) + 11)


async def redraw_shop_embed(interaction: nextcord.Interaction) -> nextcord.Embed:
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
        value=f"``` {await get_server_clan_upgrade_limit_cost(interaction.guild.id) * get_upgrade_limit_multiplier(await get_clan_member_limit(interaction.guild.id, await get_user_clan_id(interaction.guild.id, interaction.user.id)))}```",
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
        value=f"``` {await get_server_clan_change_image_cost(interaction.guild.id)}```",
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
        value=f"``` {await get_server_clan_change_icon_cost(interaction.guild.id)}```",
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
        value=f"``` {round(await get_server_clan_upgrade_attack_cost(interaction.guild.id) + (100/(2/await get_clan_min_attack(interaction.guild.id, await get_user_clan_id(interaction.guild.id, interaction.user.id))))/100)}```",
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
        f"{await get_server_clan_upgrade_boss_cost(interaction.guild.id) * get_boss_upgrade_multiplier(await get_clan_guild_boss_level(interaction.guild.id, await get_user_clan_id(interaction.guild.id, interaction.user.id)))}```",
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
        value=f"``` {await get_server_clan_change_color_cost(interaction.guild.id)}```",
        inline=True,
    )
    return embed
