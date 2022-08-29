import nextcord
import sqlite3
from core.dataclassesList import CustomRole
from core.money.updaters import update_user_balance
from typing import Coroutine, Any


async def buy_role(interaction, role: nextcord.Role) -> Coroutine[Any, Any, None]:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    balance = cursor.execute(
        f"SELECT balance FROM money WHERE guild_id = {interaction.guild.id} AND user_id = {interaction.user.id}"
    ).fetchone()[0]
    if (
            nextcord.Role is not None
            and cursor.execute(
        f"SELECT role_id FROM custom_shop WHERE guild_id = {interaction.guild.id}"
    ).fetchone()[0]
            is not None
    ):
        if role not in interaction.user.roles:
            rol = CustomRole(
                *list(cursor.execute(
                    f"SELECT * FROM custom_shop WHERE guild_id = {interaction.guild.id} AND role_id = {role.id}"
                ).fetchall()[0])
            )
            if balance >= rol.cost:
                guild_id = interaction.guild.id
                update_user_balance(guild_id, rol.owner_id, rol.cost)
                update_user_balance(guild_id, interaction.user.id, -abs(rol.cost))
                cursor.execute(
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
                await interaction.send(f"**{interaction.user.mention}**, у вас недостаточно средств")
        else:
            await interaction.send(f"**{interaction.user.mention}**, вы уже приобрели данную роль")
