import nextcord
from core.dataclassesList import CustomRole
from core.db_utils import execute_update, fetch_one
from core.money.updaters import update_user_balance
from typing import Coroutine, Any


async def delete_role_from_shop(guild: nextcord.Guild, role_id: int) -> None:
    await execute_update(
        "DELETE FROM custom_shop WHERE role_id = %s AND guild_id = %s",
        (role_id, guild.id),
    )


async def buy_role(interaction, role: nextcord.Role) -> Coroutine[Any, Any, None]:
    balance = await fetch_one(
        f"SELECT balance FROM money WHERE guild_id = {interaction.guild.id} AND user_id = {interaction.user.id}"
    )
    balance = balance[0]
    if (
        nextcord.Role is not None
        and await fetch_one(
            f"SELECT role_id FROM custom_shop WHERE guild_id = {interaction.guild.id}"
        )
        is not None
    ):
        if role not in interaction.user.roles:
            rol = CustomRole(
                *list(
                    await fetch_all(
                        f"SELECT * FROM custom_shop WHERE guild_id = {interaction.guild.id} AND role_id = {role.id}"
                    )[0]
                )
            )
            if balance >= rol.cost:
                guild_id = interaction.guild.id
                await update_user_balance(guild_id, rol.owner_id, rol.cost)
                await update_user_balance(guild_id, interaction.user.id, -abs(rol.cost))
                await execute_update(
                    f"UPDATE custom_shop SET bought = bought + 1 WHERE role_id = {role.id}"
                )

                embed = nextcord.Embed(title="Вы купили роль")
                embed.add_field(
                    name="Приобретение товара",
                    value=f"**{interaction.user.mention}**, вы приобрели роль **{role.mention}** \n \
                        Автор роли - {interaction.client.get_user(rol.owner_id).mention}",
                )
                embed.set_footer(text="Спасибо за покупку")
                await interaction.send(embed=embed, ephemeral=True)
                await interaction.user.add_roles(
                    nextcord.utils.get(interaction.guild.roles, name=role.name)
                )
            else:
                await interaction.send(
                    f"**{interaction.user.mention}**, у вас недостаточно средств"
                )
        else:
            await interaction.send(
                f"**{interaction.user.mention}**, вы уже приобрели данную роль"
            )
