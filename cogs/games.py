import datetime
import random
from typing import Optional, Union

import cooldowns
import nextcord
from nextcord import Interaction, Permissions, SlashOption
from nextcord.ext import commands

from core.bet.getters import get_max_bet, get_min_bet
from core.embeds import DEFAULT_BOT_COLOR, construct_basic_embed
from core.emojify import SWORD
from core.errors import (
    construct_error_negative_value_embed,
    construct_error_not_enough_embed,
    construct_error_command_is_active,
    construct_error_incorrect_bet,
)
from core.games.blackjack import (
    Hand,
    check_for_blackjack,
    player_is_over,
    create_deck,
    deal_starting_cards,
    create_blackjack_embed,
    create_final_view,
    maybe_blackjack_cards,
    create_game_start_blackjack_embed,
)
from core.games.gamble import (
    perform_strikes,
    compare_strikes,
    create_gamble_embed,
    approximate_bet,
    get_game_state,
)
from core.games.slots import check_win_get_multiplier, spin_slots, create_slots_embed
from core.games.ttt import TicTacToe
from core.games.wheel import (
    get_multiplier,
    construct_wheel_embed,
    spin_wheel,
    initialize_multipliers,
    get_direction,
)
from core.locales.getters import (
    get_localized_name,
    get_localized_description,
    get_guild_locale,
)
from core.locales.getters import get_msg_from_locale_by_key, localize_name
from core.money.getters import get_user_balance, get_guild_currency_symbol
from core.money.updaters import update_user_balance
from core.ui.buttons import create_button, ViewAuthorCheck

MULTIPLIERS_FOR_TWO_ROWS = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]

MULTIPLIERS_FOR_THREE_ROWS = [2.0, 2.1, 2.2, 2.3, 2.4, 2.5]


class DuelEndRu(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(
        label="Дуэль",
        style=nextcord.ButtonStyle.red,
        disabled=True,
    )
    async def duel_start(self, button: nextcord.ui.Button, interaction: Interaction):
        pass


class DuelStartRu(nextcord.ui.View):
    def __init__(
            self, author: Union[nextcord.Member, nextcord.User], bet: Optional[int]
    ):
        self.author = author
        self.bet = bet
        super().__init__()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user == self.author:
            return False
        if await get_user_balance(interaction.guild.id, interaction.user.id) < self.bet:
            return False
        return True

    @nextcord.ui.button(
        label="Дуэль",
        style=nextcord.ButtonStyle.red,
        disabled=False,
    )
    async def duel_start(self, button: nextcord.ui.Button, interaction: Interaction):
        author = self.author
        user = interaction.user
        balance = await get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < self.bet:
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            await interaction.message.edit(view=DuelEndRu())
            return await interaction.response.send_message(
                embed=construct_error_not_enough_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_enough_money_error"
                    ),
                    interaction.user.display_avatar,
                    f"{msg} {balance}",
                )
            )
        balance = await get_user_balance(interaction.guild.id, author.id)
        if balance < self.bet:
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            await interaction.message.edit(view=DuelEndRu())
            return await interaction.response.send_message(
                embed=construct_error_not_enough_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_enough_money_error"
                    ),
                    author.display_avatar,
                    f"{msg} {balance}",
                )
            )
        who_win = random.choice([author, user])
        if who_win == author:
            losed = user
        else:
            losed = author
        currency = await get_guild_currency_symbol(interaction.guild.id)
        embed = nextcord.Embed(
            title=f"{SWORD} Дуэль",
            description=f"В дуэле побеждает {who_win.mention} и зарабатывает {self.bet} {currency}",
            color=DEFAULT_BOT_COLOR,
        )
        await update_user_balance(interaction.guild.id, who_win.id, self.bet)
        await update_user_balance(interaction.guild.id, losed.id, -self.bet)
        balance = await get_user_balance(interaction.guild.id, who_win.id)
        msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
        embed.set_footer(text=f"{msg} {balance}", icon_url=who_win.display_avatar)
        await interaction.message.edit(embed=embed, view=DuelEndRu())


class DuelEndEng(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(
        label="Duel",
        style=nextcord.ButtonStyle.red,
        disabled=True,
    )
    async def duel_start(self, button: nextcord.ui.Button, interaction: Interaction):
        pass


class DuelStartEng(nextcord.ui.View):
    def __init__(
            self, author: Union[nextcord.Member, nextcord.User], bet: Optional[int]
    ):
        self.author = author
        self.bet = bet
        super().__init__()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user == self.author:
            return False
        if await get_user_balance(interaction.guild.id, interaction.user.id) < self.bet:
            return False
        return True

    @nextcord.ui.button(
        label="Duel",
        style=nextcord.ButtonStyle.red,
        disabled=False,
    )
    async def duel_start(self, button: nextcord.ui.Button, interaction: Interaction):
        author = self.author
        user = interaction.user
        balance = await get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < self.bet:
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            await interaction.message.edit(view=DuelEndRu())
            return await interaction.response.send_message(
                embed=construct_error_not_enough_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_enough_money_error"
                    ),
                    interaction.user.display_avatar,
                    f"{msg} {balance}",
                )
            )
        balance = await get_user_balance(interaction.guild.id, author.id)
        if balance < self.bet:
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            await interaction.message.edit(view=DuelEndRu())
            return await interaction.response.send_message(
                embed=construct_error_not_enough_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_enough_money_error"
                    ),
                    author.display_avatar,
                    f"{msg} {balance}",
                )
            )
        who_win = random.choice([author, user])
        if who_win == author:
            losed = user
        else:
            losed = author
        currency = get_guild_currency_symbol(interaction.guild.id)
        embed = nextcord.Embed(
            title=f"{SWORD} Duel",
            description=f"In duel **won** {who_win.mention} and this user get **{self.bet}** {currency}",
            color=DEFAULT_BOT_COLOR,
        )
        await update_user_balance(interaction.guild.id, who_win.id, self.bet)
        await update_user_balance(interaction.guild.id, losed.id, -self.bet)
        balance = await get_user_balance(interaction.guild.id, who_win.id)
        msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
        embed.set_footer(text=f"{msg} {balance}", icon_url=who_win.display_avatar)
        await interaction.message.edit(embed=embed, view=DuelEndEng())


class Games(commands.Cog):
    def __init__(self, client):
        self.users = dict()
        self.client = client

    @nextcord.slash_command(
        name="blackjack",
        description="Play blackjack casino game",
        name_localizations=get_localized_name("blackjack"),
        description_localizations=get_localized_description("blackjack"),
        default_member_permissions=Permissions(send_messages=True),
    )
    @cooldowns.cooldown(1, 3, bucket=cooldowns.SlashBucket.author)
    async def __blackjack(
            self,
            interaction: Interaction,
            bet: Optional[int] = SlashOption(
                required=True,
                description="Number of money you bet in game",
                description_localizations={
                    "ru": "Количество денег, которое вы хотите поставить в качестве ставки"
                },
            ),
    ):
        await interaction.response.defer()
        if bet <= 0:
            return await interaction.followup.send(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    bet,
                )
            )
        bet_min, bet_max = await get_min_bet(interaction.guild.id), await get_max_bet(interaction.guild.id)
        if bet < bet_min or bet > bet_max:
            return await interaction.followup.send(
                embed=construct_error_incorrect_bet(
                    f'{get_msg_from_locale_by_key(interaction.guild.id, "bet_range_error")} '
                    f'**{bet_min}** - **{bet_max}** {get_guild_currency_symbol(interaction.guild.id)}',
                    interaction.user.display_avatar,
                )
            )
        balance = await get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < bet:
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            return await interaction.followup.send(
                embed=construct_error_not_enough_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "not_enough_money_error"
                    ),
                    interaction.user.display_avatar,
                    f"{msg} {balance}/{bet}",
                )
            )
        global player
        player = interaction.user
        deck = create_deck()
        player_hand = Hand()
        dealer_hand = Hand(dealer=True)
        deal_starting_cards(player_hand, dealer_hand, deck)
        global turn
        turn = 1
        timestamp = datetime.datetime.now().timestamp()
        user = self.users.get(interaction.user.id, None)
        if user is None:
            self.users.update({interaction.user.id: timestamp})
        if user is not None:
            if timestamp - user < 120:
                return await interaction.followup.send(
                    embed=construct_error_command_is_active(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "command_is_active_error"
                        ),
                        interaction.user.display_avatar,
                    )
                )

        async def hit_callback(interaction: Interaction):
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < bet:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                view = create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                return await interaction.message.edit(embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    ), view=view)
            global turn
            turn += 1
            player_hand.add_card(deck.deal())
            if player_is_over(player_hand):
                await update_user_balance(interaction.guild.id, interaction.user.id, -bet)
                balance = await get_user_balance(interaction.guild.id, interaction.user.id)
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
                embed = await create_blackjack_embed(
                    self.client,
                    f"{self.client.user.mention} {win}",
                    player_hand,
                    dealer_hand,
                    f"{msg} {balance}",
                    interaction.user.display_avatar,
                    guild_id=interaction.guild.id,
                )
                view = await create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                await interaction.message.edit(embed=embed, view=view)
            else:
                turn_msg = get_msg_from_locale_by_key(interaction.guild.id, "turn")
                embed = await create_game_start_blackjack_embed(
                    self.client,
                    f"{turn_msg} {turn}",
                    player_hand,
                    dealer_hand,
                    guild_id=interaction.guild.id,
                )
                await interaction.message.edit(embed=embed)

        async def stand_callback(interaction: Interaction):
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < bet:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                view = await create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                return await interaction.message.edit(embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    ), view=view)
            global turn
            turn += 1
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal())
                if player_is_over(dealer_hand):
                    await update_user_balance(interaction.guild.id, interaction.user.id, bet)
                    balance = await get_user_balance(
                        interaction.guild.id, interaction.user.id
                    )
                    msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                    win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                    embed = await create_blackjack_embed(
                        self.client,
                        f"**{interaction.user.mention}** {win}",
                        player_hand,
                        dealer_hand,
                        f"{msg} {balance}",
                        interaction.user.display_avatar,
                        guild_id=interaction.guild.id,
                    )
                    view = await create_final_view(interaction.guild.id)
                    self.users.pop(interaction.user.id)
                    await interaction.message.edit(embed=embed, view=view)
            if 17 <= dealer_hand.get_value() <= 21:
                if dealer_hand.get_value() > player_hand.get_value():
                    await update_user_balance(interaction.guild.id, interaction.user.id, -bet)
                    balance = await get_user_balance(
                        interaction.guild.id, interaction.user.id
                    )
                    msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                    win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                    lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
                    embed = await create_blackjack_embed(
                        self.client,
                        f"{self.client.user.mention} {win}",
                        player_hand,
                        dealer_hand,
                        f"{msg} {balance}",
                        interaction.user.display_avatar,
                        guild_id=interaction.guild.id,
                    )
                    view = await create_final_view(interaction.guild.id)
                    self.users.pop(interaction.user.id)
                    await interaction.message.edit(embed=embed, view=view)
                elif dealer_hand.get_value() == player_hand.get_value():
                    draw = get_msg_from_locale_by_key(interaction.guild.id, "draw")
                    embed = await create_blackjack_embed(
                        self.client,
                        f"**{draw}**",
                        player_hand,
                        dealer_hand,
                        guild_id=interaction.guild.id,
                    )
                    view = await create_final_view(interaction.guild.id)
                    self.users.pop(interaction.user.id)
                    await interaction.message.edit(embed=embed, view=view)
                else:
                    await update_user_balance(interaction.guild.id, interaction.user.id, bet)
                    balance = await get_user_balance(
                        interaction.guild.id, interaction.user.id
                    )
                    msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                    win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                    lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
                    embed = await create_blackjack_embed(
                        self.client,
                        f"**{interaction.user.mention}** {win}",
                        player_hand,
                        dealer_hand,
                        f"{msg} {balance}",
                        interaction.user.display_avatar,
                        guild_id=interaction.guild.id,
                    )
                    view = await create_final_view(interaction.guild.id)
                    self.users.pop(interaction.user.id)
                    await interaction.message.edit(embed=embed, view=view)

        async def dealer_blackjack_callback(interaction: Interaction):
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < bet:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                view = await create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                return await interaction.message.edit(embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    ), view=view)
            if check_for_blackjack(dealer_hand):
                draw = get_msg_from_locale_by_key(interaction.guild.id, "draw")
                embed = await create_blackjack_embed(
                    self.client,
                    f"**{draw}**",
                    player_hand,
                    dealer_hand,
                    guild_id=interaction.guild.id,
                )
                view = await create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                await interaction.message.edit(embed=embed, view=view)
            else:
                await update_user_balance(
                    interaction.guild.id, interaction.user.id, int(bet * 1.5)
                )
                balance = await get_user_balance(interaction.guild.id, interaction.user.id)
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
                embed = await create_blackjack_embed(
                    self.client,
                    f"**{interaction.user.mention}** {win}",
                    player_hand,
                    dealer_hand,
                    f"{msg} {balance}",
                    interaction.user.display_avatar,
                    guild_id=interaction.guild.id,
                )
                view = await create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                await interaction.message.edit(embed=embed, view=view)

        async def one_to_one_callback(interaction: Interaction):
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < bet:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                view = await create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                return await interaction.message.edit(embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    ), view=view)
            await update_user_balance(interaction.guild.id, interaction.user.id, bet)
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
            one_to_one_msg = get_msg_from_locale_by_key(
                interaction.guild.id, "one_to_one"
            )
            embed = create_blackjack_embed(
                self.client,
                f"**{interaction.user.mention}** {one_to_one_msg}",
                player_hand,
                dealer_hand,
                f"{msg} {balance}",
                interaction.user.display_avatar,
                guild_id=interaction.guild.id,
            )
            view = create_final_view(interaction.guild.id)
            self.users.pop(interaction.user.id)
            await interaction.message.edit(embed=embed, view=view)

        if check_for_blackjack(player_hand):
            balance = await get_user_balance(interaction.guild.id, interaction.user.id)
            if balance < bet:
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                view = await create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                return await interaction.message.edit(embed=construct_error_not_enough_embed(
                        get_msg_from_locale_by_key(
                            interaction.guild.id, "not_enough_money_error"
                        ),
                        interaction.user.display_avatar,
                        f"{msg} {balance}",
                    ), view=view)
            if str(dealer_hand.cards[1]) in maybe_blackjack_cards:
                dealer_blackjack = create_button(
                    "Blackjack", dealer_blackjack_callback, False
                )
                one_to_one = create_button("1:1", one_to_one_callback, False)
                view = ViewAuthorCheck(interaction.user)
                view.add_item(dealer_blackjack)
                view.add_item(one_to_one)
                turn_msg = get_msg_from_locale_by_key(interaction.guild.id, "turn")
                embed = await create_game_start_blackjack_embed(
                    self.client,
                    f"{turn_msg} {turn}",
                    player_hand,
                    dealer_hand,
                    guild_id=interaction.guild.id,
                )
                await interaction.followup.send(embed=embed, view=view)
            else:
                await update_user_balance(
                    interaction.guild.id, interaction.user.id, int(bet * 1.5)
                )
                balance = await get_user_balance(interaction.guild.id, interaction.user.id)
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
                    guild_id=interaction.guild.id,
                )
                view = await create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                await interaction.followup.send(embed=embed, view=view)
        else:
            if check_for_blackjack(dealer_hand):
                await update_user_balance(interaction.guild.id, interaction.user.id, -bet)
                balance = await get_user_balance(interaction.guild.id, interaction.user.id)
                msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
                win = get_msg_from_locale_by_key(interaction.guild.id, "win")
                lost = get_msg_from_locale_by_key(interaction.guild.id, "lost")
                embed = await create_blackjack_embed(
                    self.client,
                    f"{self.client.user.mention} {win}",
                    player_hand,
                    dealer_hand,
                    f"{msg} {balance}",
                    interaction.user.display_avatar,
                    guild_id=interaction.guild.id,
                )
                view = await create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
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
                embed = await create_game_start_blackjack_embed(
                    self.client,
                    f"{turn_msg} {turn}",
                    player_hand,
                    dealer_hand,
                    guild_id=interaction.guild.id,
                )
                await interaction.followup.send(embed=embed, view=view)

    @nextcord.slash_command(
        name="slots",
        description="Play slots casino game",
        name_localizations=get_localized_name("slots"),
        description_localizations=get_localized_description("slots"),
        default_member_permissions=Permissions(send_messages=True),
    )
    @cooldowns.cooldown(1, 3, bucket=cooldowns.SlashBucket.author)
    async def __slots(
            self,
            interaction: Interaction,
            bet: Optional[int] = SlashOption(
                required=True,
                description="Number of money you bet in game",
                description_localizations={
                    "ru": "Количество денег, которое вы хотите поставить в качестве ставки"
                },
            ),
    ):
        if bet <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    bet,
                )
            )
        bet_min, bet_max = await get_min_bet(interaction.guild.id), await get_max_bet(interaction.guild.id)
        if bet < bet_min or bet > bet_max:
            return await interaction.response.send_message(
                embed=construct_error_incorrect_bet(
                    f'{get_msg_from_locale_by_key(interaction.guild.id, "bet_range_error")} '
                    f'**{bet_min}** - **{bet_max}** {await get_guild_currency_symbol(interaction.guild.id)}',
                    interaction.user.display_avatar,
                )
            )
        balance = await get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < bet:
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
        player_got_row = spin_slots()
        is_win, multiplier = check_win_get_multiplier(player_got_row)
        if is_win is True:
            win = get_msg_from_locale_by_key(interaction.guild.id, "win")
            game_state = f"{interaction.user.mention} **{win}**"
            bet *= multiplier
            await update_user_balance(interaction.guild.id, interaction.user.id, int(bet))
            embed = await create_slots_embed(
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
            await update_user_balance(interaction.guild.id, interaction.user.id, -int(bet))
            embed = await create_slots_embed(
                interaction.guild.id,
                interaction.user.id,
                interaction.user.display_avatar,
                interaction.application_command.name,
                player_got_row,
                game_state,
            )
            await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="gamble",
        description="Play gamble casino game",
        name_localizations=get_localized_name("gamble"),
        description_localizations=get_localized_description("gamble"),
        default_member_permissions=Permissions(send_messages=True),
    )
    @cooldowns.cooldown(1, 3, bucket=cooldowns.SlashBucket.author)
    async def __gamble(
            self,
            interaction: Interaction,
            bet: Optional[int] = SlashOption(
                required=True,
                description="Number of money you bet in game",
                description_localizations={
                    "ru": "Количество денег, которое вы хотите поставить в качестве ставки"
                },
            ),
    ):
        if bet <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    bet,
                )
            )
        bet_min, bet_max = await get_min_bet(interaction.guild.id), await get_max_bet(interaction.guild.id)
        if bet < bet_min or bet > bet_max:
            return await interaction.response.send_message(
                embed=construct_error_incorrect_bet(
                    f'{get_msg_from_locale_by_key(interaction.guild.id, "bet_range_error")} '
                    f'**{bet_min}** - **{bet_max}** {get_guild_currency_symbol(interaction.guild.id)}',
                    interaction.user.display_avatar,
                )
            )
        balance = await get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < bet:
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
        user_strikes, bot_strikes = perform_strikes()
        is_win = compare_strikes(user_strikes, bot_strikes)
        percentage, bet = approximate_bet(bet, is_win)
        if is_win is True:
            await update_user_balance(interaction.guild.id, interaction.user.id, int(bet))
        if is_win is False:
            await update_user_balance(interaction.guild.id, interaction.user.id, -int(bet))
        msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
        balance = await get_user_balance(interaction.guild.id, interaction.user.id)
        game_state = await get_game_state(
            is_win, interaction.user, self.client, interaction.guild.id
        )
        embed = await create_gamble_embed(
            is_win,
            game_state,
            percentage,
            user_strikes,
            bot_strikes,
            f"{msg} {balance}",
            interaction.user.display_avatar,
            interaction.guild.id,
        )
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="wheel",
        description="Spin wheel casino game",
        name_localizations=get_localized_name("wheel"),
        description_localizations=get_localized_description("wheel"),
        default_member_permissions=Permissions(send_messages=True),
    )
    @cooldowns.cooldown(1, 3, bucket=cooldowns.SlashBucket.author)
    async def __wheel(
            self,
            interaction: Interaction,
            bet: Optional[int] = SlashOption(
                required=True,
                description="Number of money you bet in game",
                description_localizations={
                    "ru": "Количество денег, которое вы хотите поставить в качестве ставки"
                },
            ),
    ):
        if bet <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    bet,
                )
            )
        bet_min, bet_max = await get_min_bet(interaction.guild.id), await get_max_bet(interaction.guild.id)
        if bet < bet_min or bet > bet_max:
            return await interaction.response.send_message(
                embed=construct_error_incorrect_bet(
                    f'{get_msg_from_locale_by_key(interaction.guild.id, "bet_range_error")} '
                    f'**{bet_min}** - **{bet_max}** {await get_guild_currency_symbol(interaction.guild.id)}',
                    interaction.user.display_avatar,
                )
            )
        balance = await get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < bet:
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
        await update_user_balance(interaction.guild.id, interaction.user.id, -int(bet))
        multipliers = initialize_multipliers()
        wheel_number = spin_wheel()
        bet_multiplier = get_multiplier(multipliers, wheel_number)
        await update_user_balance(
            interaction.guild.id, interaction.user.id, (int(bet * bet_multiplier))
        )
        msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
        balance = await get_user_balance(interaction.guild.id, interaction.user.id)
        await interaction.response.send_message(
            embed=construct_wheel_embed(
                interaction.application_command.name.capitalize(),
                multipliers,
                get_direction(wheel_number),
                f"{msg} {balance}",
                interaction.user.display_avatar,
            )
        )

    @nextcord.slash_command(
        name="duel",
        description="duel",
        name_localizations=get_localized_name("duel"),
        description_localizations=get_localized_description("duel"),
        default_member_permissions=Permissions(send_messages=True),
    )
    @cooldowns.cooldown(1, 3, bucket=cooldowns.SlashBucket.author)
    async def __duel(
            self,
            interaction: Interaction,
            bet: Optional[int] = SlashOption(
                required=True,
                description="Number of money you bet in game",
                description_localizations={
                    "ru": "Количество денег, которое вы хотите поставить в качестве ставки"
                },
            ),
    ):
        if bet <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    bet,
                )
            )
        bet_min, bet_max = await get_min_bet(interaction.guild.id), await get_max_bet(interaction.guild.id)
        if bet < bet_min or bet > bet_max:
            return await interaction.response.send_message(
                embed=construct_error_incorrect_bet(
                    f'{get_msg_from_locale_by_key(interaction.guild.id, "bet_range_error")} '
                    f'**{bet_min}** - **{bet_max}** {await get_guild_currency_symbol(interaction.guild.id)}',
                    interaction.user.display_avatar,
                )
            )
        balance = await get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < bet:
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
        embed = nextcord.Embed(
            title=f"{SWORD} {localize_name(interaction.guild.id, 'duel').capitalize()}",
            description=f"{interaction.user.mention} {get_msg_from_locale_by_key(interaction.guild.id, 'duel')} **{bet}** "
                        f"{await get_guild_currency_symbol(interaction.guild.id)}",
            color=DEFAULT_BOT_COLOR,
        )
        if get_guild_locale(interaction.guild.id) == "ru_ru":
            await interaction.response.send_message(
                embed=embed, view=DuelStartRu(interaction.user, bet)
            )
        else:
            await interaction.response.send_message(
                embed=embed, view=DuelStartEng(interaction.user, bet)
            )

    @nextcord.slash_command(
        name="ttt",
        description="ttt",
        name_localizations=get_localized_name("ttt"),
        description_localizations=get_localized_description("ttt"),
        default_member_permissions=Permissions(send_messages=True),
    )
    async def __ttt(self, interaction: Interaction,
                    bet: Optional[int] = SlashOption(
                        required=True,
                        description="Number of money you bet in game",
                        description_localizations={
                            "ru": "Количество денег, которое вы хотите поставить в качестве ставки"
                        },
                    )
                    ):
        if bet <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    get_msg_from_locale_by_key(
                        interaction.guild.id, "negative_value_error"
                    ),
                    self.client.user.avatar.url,
                    bet,
                )
            )
        bet_min, bet_max = await get_min_bet(interaction.guild.id), await get_max_bet(interaction.guild.id)
        if bet < bet_min or bet > bet_max:
            return await interaction.response.send_message(
                embed=construct_error_incorrect_bet(
                    f'{get_msg_from_locale_by_key(interaction.guild.id, "bet_range_error")} '
                    f'**{bet_min}** - **{bet_max}** {await get_guild_currency_symbol(interaction.guild.id)}',
                    interaction.user.display_avatar,
                )
            )
        balance = await get_user_balance(interaction.guild.id, interaction.user.id)
        if balance < bet:
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
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        embed = construct_basic_embed(
            "O | ☓",
            f"_ _",
            f"{requested} {interaction.user}",
            interaction.user.display_avatar,
            interaction.guild.id,
        )
        await interaction.send(embed=embed, view=TicTacToe(author=interaction.user, bet=bet))

    @nextcord.slash_command(name='hangman',
                            name_localizations=get_localized_name("hangman"),
                            description_localizations=get_localized_description("hangman"),
                            default_member_permissions=Permissions(send_messages=True),
                            )
    @cooldowns.cooldown(1, 60, cooldowns.SlashBucket.author)
    async def __hangman(self, interaction: Interaction):
        word_list = ['питон',
                     'анаконда',
                     'змея',
                     'сова',
                     'мышь',
                     'пчела',
                     'шершень',
                     'собака',
                     'хорек',
                     'кошка',
                     'афалина',
                     'баран',
                     'нерпа',
                     'бабуин',
                     'аплодонтия',
                     'вол',
                     'верблюд',
                     'ремнезуб',
                     'бегемот',
                     'барсук',
                     'белка',
                     'гиббон',
                     'белуха',
                     'медведь',
                     'бизон',
                     'бобер',
                     'муравьед',
                     'кенгуру',
                     'валлаби',
                     'бонго',
                     'буйвол',
                     'гиена',
                     'бурозубка',
                     'бурундук',
                     'викунья',
                     'мангуст',
                     'волк',
                     'вомбат',
                     'выхухоль',
                     'газель',
                     'гамадрил',
                     'гепард',
                     'геренук',
                     'мартышка',
                     'песец',
                     'кит',
                     'горилла',
                     'зебра',
                     'тапир',
                     'гринда',
                     'гуанако',
                     'горностай',
                     'дельфин',
                     'жираф',
                     'дикдик',
                     'кабан',
                     'дзерен',
                     'осел',
                     'динго',
                     'кенгуру',
                     'норка',
                     'долгопят',
                     'еж',
                     'зубр',
                     'ирбис',
                     'тигр',
                     'какомицли',
                     'капибара',
                     'игрунка',
                     'бегемот',
                     'кашалот',
                     'коала',
                     'козел',
                     'корова',
                     'свинья',
                     'косуля',
                     'крыса',
                     'лев',
                     'леопард',
                     'гепард',
                     'летяга',
                     'лось',
                     'лошадь',
                     'конь',
                     'морж',
                     'овца',
                     'ондатра',
                     'песчанка',
                     'пони',
                     'рысь',
                     'лисица',
                     'лиса',
                     'антилопа',
                     'сайгак',
                     'соня',
                     'ленивец',
                     'шимпанзе',
                     'ягуар',
                     'як',
                     'шиншилла',
                     'акула',
                     'чайка',
                     'скумбрия',
                     'змееящерица',
                     'ястреб',
                     'варан',
                     'журавль',
                     'лев',
                     'тигр',
                     'бабочка',
                     'геккон',
                     'барсук',
                     'щука',
                     'гепард',
                     'волк',
                     'буйвол',
                     'бурундук',
                     'снегирь',
                     'крыса',
                     'альбатрос',
                     'черепаха',
                     'акула',
                     'жаба',
                     'лягушка',
                     'пищуха',
                     'кряква',
                     'утка',
                     'утконос',
                     'пиранья',
                     'пиранга',
                     'аист',
                     'уж',
                     'сом',
                     'осетр',
                     'соня',
                     'жираф',
                     'дрозд',
                     'лемминг',
                     'пенелопа',
                     'свиристель',
                     'свистун',
                     'клещ',
                     'медведь',
                     'осел',
                     'газель',
                     'хамелеон',
                     'дикобраз',
                     'ястреб',
                     'голубь',
                     'воробей',
                     'ворона',
                     'сорока',
                     'рысь',
                     'пума',
                     'бабуин',
                     'стриж',
                     'тюлень',
                     'опоссум',
                     'орлан',
                     'попугай',
                     'певун',
                     'баклан',
                     'удод',
                     'тля',
                     'моль',
                     'выдра',
                     'колибри',
                     'гну',
                     'бизон',
                     'древолаз',
                     'шелкопряд',
                     'блоха',
                     'вошь',
                     'свинья',
                     'кабан',
                     'свин',
                     'хомяк',
                     'лань',
                     'кролик',
                     'антилопа',
                     'леопард',
                     'какаду',
                     'конь',
                     'муравьед',
                     'вилорог',
                     'сельдь',
                     'ослик',
                     'ночница',
                     'саламандра',
                     'филин',
                     'сова',
                     'гадюка',
                     'морж',
                     'дятел',
                     'петух',
                     'курица',
                     'осьминог',
                     'краб',
                     'креветка',
                     'лягушка',
                     'бабочка',
                     'глухарь',
                     'гусь',
                     'кенгуру',
                     'аноа',
                     'тритон',
                     'карась',
                     'аист',
                     'бык',
                     'дзерен',
                     'синица',
                     'удав',
                     'бегемот',
                     'суслик',
                     'шпрот',
                     'енот',
                     'трясогузка',
                     'медосос',
                     'окунь',
                     'нетопырь',
                     'цапля',
                     'кукушка',
                     'рогоклюв',
                     'фазан',
                     'сипуха',
                     'зубр',
                     'кит',
                     'игуана']
        guesses = 0
        word = random.choice(word_list)
        word_list = list(word)
        blanks = ("◆" * len(word))
        blanks_list = list(blanks)
        unbox_blank = (' '.join(blanks_list))
        new_blanks_list = list(blanks)
        guess_list = []
        guess_list_unbox = (', '.join(guess_list))
        embed_formatter = nextcord.Embed(
            color=DEFAULT_BOT_COLOR
        )
        embed_formatter.set_author(name=get_msg_from_locale_by_key(interaction.guild.id, "hangman_name"))
        hangman_pictures = {
            "hangman_picture_1": """```
              _______
             |/      |
             |      
             |      
             |       
             |
            _|___```""",
            "hangman_picture_2": """```
              _______
             |/      |
             |      (_)
             |
             |
             |
            _|___```""",
            "hangman_picture_3": """```
              _______
             |/      |
             |      (_)
             |      \|
             |
             |
            _|___```""",
            "hangman_picture_4": """```
              _______
             |/      |
             |      (_)
             |      \|/
             |
             |
            _|___```""",
            "hangman_picture_5": """```
              _______
             |/      |
             |      (_)
             |      \|/
             |       |
             |
            _|___```""",
            "hangman_picture_6": """```
              _______
             |/      |
             |      (_)
             |      \|/
             |       |
             |      /
            _|___```""",
            "hangman_picture_7": """```
              _______
             |/      |
             |      (_)
             |      \|/
             |       |
             |      / \\
            _|___```"""

        }
        image = 'шо' # ничо
        animals = get_msg_from_locale_by_key(interaction.guild.id, "animals")
        info_msg = get_msg_from_locale_by_key(interaction.guild.id, "information")
        word_msg = get_msg_from_locale_by_key(interaction.guild.id, "word")
        attempts_msg = get_msg_from_locale_by_key(interaction.guild.id, "attempts")

        embed_formatter.add_field(name=animals, value=image)
        embed_formatter.add_field(name=word_msg, value=f'\n {attempts_msg}: {guesses} \n ```{unbox_blank}```')
        embed_formatter.set_footer(text=str(guess_list_unbox))
        while guesses < 7:
            embed_formatter.clear_fields()
            image = hangman_pictures[f"hangman_picture_{guesses + 1}"]
            embed_formatter.add_field(name=animals, value=image)
            embed_formatter.add_field(name=word_msg, value=f'\n {attempts_msg}: {guesses} \n ```{unbox_blank}```')
            embed_formatter.set_footer(text=str(guess_list_unbox))
            await interaction.send(embed=embed_formatter)

            russian_symbols = {'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р',
                               'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ы', 'э', 'ю', 'я'}

            def check(author):
                def inner_check(message):
                    return message.author == author and message.content.casefold() in russian_symbols

                return inner_check

            guess = await self.client.wait_for('message', check=check(interaction.user), timeout=120)
            guess = guess.content.casefold()
            if len(guess) > 1 and guess != word:
                await interaction.send(get_msg_from_locale_by_key(interaction.guild.id, "hangman_error_1"))
                guesses -= 1
            if guess == " ":
                await interaction.send(get_msg_from_locale_by_key(interaction.guild.id, "hangman_error_2"))
            if guess in guess_list:
                await interaction.send(get_msg_from_locale_by_key(interaction.guild.id, "hangman_error_3"))
            else:
                if len(guess) == 1:
                    guess_list.append(guess)
                    guess_list_unbox = (', '.join(guess_list))
                i = 0
                while i < len(word):
                    if guess == word[i]:
                        new_blanks_list[i] = word_list[i]
                    i = i + 1

                if new_blanks_list == blanks_list:
                    guesses = guesses + 1

                if word_list != blanks_list:
                    blanks_list = new_blanks_list[:]
                    unbox_blank = (' '.join(blanks_list))

                    if word_list == blanks_list or guess == word:
                        embed_formatter.clear_fields()
                        embed_formatter.add_field(name=animals, value=image)
                        embed_formatter.add_field(name=f'{info_msg}',
                                                  value=f'\n {attempts_msg}: {guesses} \n ```{unbox_blank}```')
                        embed_formatter.set_footer(text=str(guess_list_unbox))
                        await interaction.send(embed=embed_formatter)
                        await interaction.send(f'{interaction.user.mention} '
                                               f'{get_msg_from_locale_by_key(interaction.guild.id, "win")}! ')
                        break
        if guesses == 7:
            await interaction.send(f'{interaction.user.mention} '
                                   f'{get_msg_from_locale_by_key(interaction.guild.id, "lost")}! '
                                   f'{get_msg_from_locale_by_key(interaction.guild.id, "hangman_word_was")}: {word}')


def setup(client):
    client.add_cog(Games(client))
