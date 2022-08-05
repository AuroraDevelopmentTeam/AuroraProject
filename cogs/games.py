from typing import Optional
import random

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle, File, Permissions, SlashOption
from nextcord.ui import Button, View

from core.locales.getters import get_localized_name, get_localized_description, get_msg_from_locale_by_key
from core.games.blackjack import (
    Hand,
    Deck,
    check_for_blackjack,
    show_blackjack_results,
    player_is_over,
    cards_emoji_representation,
    create_deck,
    deal_starting_cards,
    create_blackjack_embed,
    create_final_view,
    maybe_blackjack_cards,
    create_game_start_blackjack_embed,
)
from core.games.slots import check_win_get_multiplier, spin_slots, create_slots_embed
from core.games.brick_knife_evidence_yandere_tentacles import (
    create_starting_embed,
    create_starting_view,
)
from core.games.gamble import (
    perform_strikes,
    compare_strikes,
    create_gamble_embed,
    approximate_bet,
    get_game_state,
)
from core.games.wheel import (
    get_multiplier,
    construct_wheel_embed,
    spin_wheel,
    initialize_multipliers,
    get_direction,
)
from core.ui.buttons import create_button, ViewAuthorCheck
from core.locales.getters import get_msg_from_locale_by_key
from core.money.updaters import update_user_balance
from core.money.getters import get_user_balance, get_guild_currency_symbol

MULTIPLIERS_FOR_TWO_ROWS = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]

MULTIPLIERS_FOR_THREE_ROWS = [2.0, 2.1, 2.2, 2.3, 2.4, 2.5]


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="blackjack",
        description="Play blackjack casino game",
        name_localizations=get_localized_name("blackjack"),
        description_localizations=get_localized_description("blackjack"),
        default_member_permissions=Permissions(send_messages=True)
    )
    async def __blackjack(
            self, interaction: Interaction,
            bet: Optional[int] = SlashOption(
                required=True,
                description="Number of money you bet in game",
                description_localizations={"ru": "Количество денег, которое вы хотите поставить в качестве ставки"},
            )
    ):
        await interaction.response.defer()
        if bet <= 0:
            return await interaction.followup.send("negative_value_error")
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < bet:
            return await interaction.followup.send("not_enough_money_error")
        global player
        player = interaction.user
        deck = create_deck()
        player_hand = Hand()
        dealer_hand = Hand(dealer=True)
        deal_starting_cards(player_hand, dealer_hand, deck)
        global turn
        turn = 1

        async def hit_callback(interaction: Interaction):
            global turn
            turn += 1
            player_hand.add_card(deck.deal())
            if player_is_over(player_hand):
                update_user_balance(interaction.guild.id, interaction.user.id, -bet)
                balance = get_user_balance(interaction.guild.id, interaction.user.id)
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
                embed = create_blackjack_embed(
                    self.client,
                    f"{self.client.user.mention} {win}",
                    player_hand,
                    dealer_hand,
                    f"{msg} {balance}",
                    interaction.user.display_avatar,
                    guild_id=interaction.guild.id
                )
                view = create_final_view(interaction.guild.id)
                await interaction.message.edit(embed=embed, view=view)
            else:
                turn_msg = get_msg_from_locale_by_key(interaction.guild.id, "turn")
                embed = create_game_start_blackjack_embed(
                    self.client, f"{turn_msg} {turn}", player_hand, dealer_hand, guild_id=interaction.guild.id
                )
                await interaction.message.edit(embed=embed)

        async def stand_callback(interaction: Interaction):
            global turn
            turn += 1
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal())
                if player_is_over(dealer_hand):
                    update_user_balance(interaction.guild.id, interaction.user.id, bet)
                    balance = get_user_balance(
                        interaction.guild.id, interaction.user.id
                    )
                    msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                    win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                    embed = create_blackjack_embed(
                        self.client,
                        f"**{interaction.user.mention}** {win}",
                        player_hand,
                        dealer_hand,
                        f"{msg} {balance}",
                        interaction.user.display_avatar,
                        guild_id=interaction.guild.id
                    )
                    view = create_final_view(interaction.guild.id)
                    await interaction.message.edit(embed=embed, view=view)
            if 17 <= dealer_hand.get_value() <= 21:
                if dealer_hand.get_value() > player_hand.get_value():
                    update_user_balance(interaction.guild.id, interaction.user.id, -bet)
                    balance = get_user_balance(
                        interaction.guild.id, interaction.user.id
                    )
                    msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                    win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                    lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
                    embed = create_blackjack_embed(
                        self.client,
                        f"{self.client.user.mention} {win}",
                        player_hand,
                        dealer_hand,
                        f"{msg} {balance}",
                        interaction.user.display_avatar,
                        guild_id=interaction.guild.id
                    )
                    view = create_final_view(interaction.guild.id)
                    await interaction.message.edit(embed=embed, view=view)
                elif dealer_hand.get_value() == player_hand.get_value():
                    draw = get_msg_from_locale_by_key(interaction.guild.id, "draw")
                    embed = create_blackjack_embed(
                        self.client, f"**{draw}**", player_hand, dealer_hand, guild_id=interaction.guild.id
                    )
                    view = create_final_view(interaction.guild.id)
                    await interaction.message.edit(embed=embed, view=view)
                else:
                    update_user_balance(interaction.guild.id, interaction.user.id, bet)
                    balance = get_user_balance(
                        interaction.guild.id, interaction.user.id
                    )
                    msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                    win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                    lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
                    embed = create_blackjack_embed(
                        self.client,
                        f"**{interaction.user.mention}** {win}",
                        player_hand,
                        dealer_hand,
                        f"{msg} {balance}",
                        interaction.user.display_avatar,
                        guild_id=interaction.guild.id
                    )
                    view = create_final_view(interaction.guild.id)
                    await interaction.message.edit(embed=embed, view=view)

        async def dealer_blackjack_callback(interaction: Interaction):
            if check_for_blackjack(dealer_hand):
                draw = get_msg_from_locale_by_key(interaction.guild.id, "draw")
                embed = create_blackjack_embed(
                    self.client, f"**{draw}**", player_hand, dealer_hand, guild_id=interaction.guild.id
                )
                view = create_final_view(interaction.guild.id)
                await interaction.message.edit(embed=embed, view=view)
            else:
                update_user_balance(
                    interaction.guild.id, interaction.user.id, int(bet * 1.5)
                )
                balance = get_user_balance(interaction.guild.id, interaction.user.id)
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
                embed = create_blackjack_embed(
                    self.client,
                    f"**{interaction.user.mention}** {win}",
                    player_hand,
                    dealer_hand,
                    f"{msg} {balance}",
                    interaction.user.display_avatar,
                    guild_id=interaction.guild.id
                )
                view = create_final_view(interaction.guild.id)
                await interaction.message.edit(embed=embed, view=view)

        async def one_to_one_callback(interaction: Interaction):
            update_user_balance(interaction.guild.id, interaction.user.id, bet)
            balance = get_user_balance(interaction.guild.id, interaction.user.id)
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            one_to_one_msg = get_msg_from_locale_by_key(interaction.guild.id, "one_to_one")
            embed = create_blackjack_embed(
                self.client,
                f"**{interaction.user.mention}** {one_to_one_msg}",
                player_hand,
                dealer_hand,
                f"{msg} {balance}",
                interaction.user.display_avatar,
                guild_id=interaction.guild.id
            )
            view = create_final_view(interaction.guild.id)
            await interaction.message.edit(embed=embed, view=view)

        if check_for_blackjack(player_hand):
            if str(dealer_hand.cards[1]) in maybe_blackjack_cards:
                dealer_blackjack = create_button(
                    "Blackjack", dealer_blackjack_callback, False
                )
                one_to_one = create_button("1:1", one_to_one_callback, False)
                view = ViewAuthorCheck(interaction.user)
                view.add_item(dealer_blackjack)
                view.add_item(one_to_one)
                turn_msg = get_msg_from_locale_by_key(interaction.guild.id, "turn")
                embed = create_game_start_blackjack_embed(
                    self.client, f"{turn_msg} {turn}", player_hand, dealer_hand, guild_id=interaction.guild.id
                )
                await interaction.followup.send(embed=embed, view=view)
            else:
                update_user_balance(
                    interaction.guild.id, interaction.user.id, int(bet * 1.5)
                )
                balance = get_user_balance(interaction.guild.id, interaction.user.id)
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
                embed = create_blackjack_embed(
                    self.client,
                    f"**{interaction.user.mention}** {win}",
                    player_hand,
                    dealer_hand,
                    f"{msg} {balance}",
                    interaction.user.display_avatar,
                    guild_id=interaction.guild.id
                )
                view = create_final_view(interaction.guild.id)
                await interaction.followup.send(embed=embed, view=view)
        else:
            if check_for_blackjack(dealer_hand):
                update_user_balance(interaction.guild.id, interaction.user.id, -bet)
                balance = get_user_balance(interaction.guild.id, interaction.user.id)
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
                embed = create_blackjack_embed(
                    self.client,
                    f"{self.client.user.mention} {win}",
                    player_hand,
                    dealer_hand,
                    f"{msg} {balance}",
                    interaction.user.display_avatar,
                    guild_id=interaction.guild.id
                )
                view = create_final_view(interaction.guild.id)
                await interaction.followup.send(embed=embed, view=view)
            else:
                hit_msg = get_msg_from_locale_by_key(interaction.guild.id, "hit")
                stand_msg = get_msg_from_locale_by_key(interaction.guild.id, "stand")
                hit = create_button(hit_msg, hit_callback, False)
                stand = create_button(stand_msg, stand_callback, False)
                view = ViewAuthorCheck(interaction.user)
                view.add_item(hit)
                view.add_item(stand)
                turn_msg = get_msg_from_locale_by_key(interaction.guild.id, "turn")
                embed = create_game_start_blackjack_embed(
                    self.client, f"{turn_msg} {turn}", player_hand, dealer_hand, guild_id=interaction.guild.id
                )
                await interaction.followup.send(embed=embed, view=view)

    @nextcord.slash_command(
        name="slots",
        description="Play slots casino game",
        name_localizations=get_localized_name("slots"),
        description_localizations=get_localized_description("slots"),
        default_member_permissions=Permissions(send_messages=True)
    )
    async def __slots(
            self, interaction: Interaction,
            bet: Optional[int] = SlashOption(
                required=True,
                description="Number of money you bet in game",
                description_localizations={"ru": "Количество денег, которое вы хотите поставить в качестве ставки"},
            )
    ):
        player_got_row = spin_slots()
        is_win, multiplier = check_win_get_multiplier(player_got_row)
        if is_win is True:
            win = get_msg_from_locale_by_key(interaction.guild.id, "win")
            game_state = f'{interaction.user.mention} **{win}**'
            bet *= multiplier
            update_user_balance(interaction.guild.id, interaction.user.id, int(bet))
            embed = create_slots_embed(
                interaction.guild.id,
                interaction.user.id,
                interaction.user.display_avatar,
                interaction.application_command.name,
                player_got_row,
                game_state,
            )
            await interaction.response.send_message(embed=embed)
        else:
            lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
            game_state = f"{interaction.user.mention} **{lost}**"
            update_user_balance(interaction.guild.id, interaction.user.id, -int(bet))
            embed = create_slots_embed(
                interaction.guild.id,
                interaction.user.id,
                interaction.user.display_avatar,
                interaction.application_command.name,
                player_got_row,
                game_state,
            )
            await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="brick_knife_evidence_yandere",
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __brick_knife_evidence_yandere_tentacles(self, interaction: Interaction):
        await interaction.response.defer()
        embed = create_starting_embed(
            "Brick Knife Evidence Yandere Tentacles",
            "Pick 1 of 5 options and see that's will happen",
        )
        view = create_starting_view()
        await interaction.followup.send(embed=embed, view=view)

    @nextcord.slash_command(
        name="gamble",
        description="Play gamble casino game",
        name_localizations=get_localized_name("gamble"),
        description_localizations=get_localized_description("gamble"),
        default_member_permissions=Permissions(send_messages=True)
    )
    async def __gamble(
            self, interaction: Interaction,
            bet: Optional[int] = SlashOption(
                required=True,
                description="Number of money you bet in game",
                description_localizations={"ru": "Количество денег, которое вы хотите поставить в качестве ставки"},
            )
    ):
        if bet <= 0:
            return await interaction.response.send_message("negative_value_error")
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < bet:
            return await interaction.response.send_message("not_enough_money_error")
        user_strikes, bot_strikes = perform_strikes()
        is_win = compare_strikes(user_strikes, bot_strikes)
        percentage, bet = approximate_bet(bet, is_win)
        if is_win is True:
            update_user_balance(interaction.guild.id, interaction.user.id, int(bet))
        if is_win is False:
            update_user_balance(interaction.guild.id, interaction.user.id, -int(bet))
        msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        game_state = get_game_state(is_win, interaction.user, self.client, interaction.guild.id)
        embed = create_gamble_embed(
            is_win,
            game_state,
            percentage,
            user_strikes,
            bot_strikes,
            f"{msg} {balance}",
            interaction.user.display_avatar,
            interaction.guild.id
        )
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="wheel",
        description="Spin wheel casino game",
        name_localizations=get_localized_name("wheel"),
        description_localizations=get_localized_description("wheel"),
        default_member_permissions=Permissions(send_messages=True)
    )
    async def __wheel(
            self, interaction: Interaction,
            bet: Optional[int] = SlashOption(
                required=True,
                description="Number of money you bet in game",
                description_localizations={"ru": "Количество денег, которое вы хотите поставить в качестве ставки"},
            )
    ):
        if bet <= 0:
            return await interaction.response.send_message("negative_value_error")
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < bet:
            return await interaction.response.send_message("not_enough_money_error")
        update_user_balance(interaction.guild.id, interaction.user.id, -int(bet))
        multipliers = initialize_multipliers()
        wheel_number = spin_wheel()
        bet_multiplier = get_multiplier(multipliers, wheel_number)
        update_user_balance(
            interaction.guild.id, interaction.user.id, (int(bet * bet_multiplier))
        )
        msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
        balance = get_user_balance(interaction.guild.id, interaction.user.id)
        await interaction.response.send_message(
            embed=construct_wheel_embed(
                interaction.application_command.name.capitalize(),
                multipliers,
                get_direction(wheel_number),
                f"{msg} {balance}",
                interaction.user.display_avatar,
            )
        )


def setup(client):
    client.add_cog(Games(client))
