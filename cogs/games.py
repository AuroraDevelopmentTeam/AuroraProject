import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle, File, Permissions
from nextcord.ui import Button, View

from core.games.blackjack import Hand, Deck, check_for_blackjack, show_blackjack_results, player_is_over, \
    cards_emoji_representation, create_deck, deal_starting_cards, create_blackjack_embed, create_final_view, \
    maybe_blackjack_cards, create_game_start_blackjack_embed
from core.games.slots import check_win_get_multiplier, spin_slots, create_slots_embed
from core.games.brick_knife_evidence_yandere_tentacles import create_starting_embed, create_starting_view
from core.ui.buttons import create_button


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name='blackjack',
                            default_member_permissions=Permissions(send_messages=True))
    async def __blackjack(self, interaction: Interaction):
        await interaction.response.defer()
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
                embed = create_blackjack_embed(self.client, "**Dealer** wins", player_hand, dealer_hand)
                view = create_final_view()
                await interaction.message.edit(embed=embed, view=view)
            else:
                embed = create_game_start_blackjack_embed(self.client, f"turn {turn}", player_hand, dealer_hand)
                await interaction.message.edit(embed=embed)

        async def stand_callback(interaction: Interaction):
            global turn
            turn += 1
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal())
                if player_is_over(dealer_hand):
                    embed = create_blackjack_embed(self.client, "**Player** wins", player_hand, dealer_hand)
                    view = create_final_view()
                    await interaction.message.edit(embed=embed, view=view)
            if 17 <= dealer_hand.get_value() <= 21:
                if dealer_hand.get_value() > player_hand.get_value():
                    embed = create_blackjack_embed(self.client, "**Dealer** wins", player_hand, dealer_hand)
                    view = create_final_view()
                    await interaction.message.edit(embed=embed, view=view)
                elif dealer_hand.get_value() == player_hand.get_value():
                    embed = create_blackjack_embed(self.client, "**Draw**", player_hand, dealer_hand)
                    view = create_final_view()
                    await interaction.message.edit(embed=embed, view=view)
                else:
                    embed = create_blackjack_embed(self.client, "**Player** wins", player_hand, dealer_hand)
                    view = create_final_view()
                    await interaction.message.edit(embed=embed, view=view)

        async def dealer_blackjack_callback(interaction: Interaction):
            if check_for_blackjack(dealer_hand):
                embed = create_blackjack_embed(self.client, "**Draw**", player_hand, dealer_hand)
                view = create_final_view()
                await interaction.message.edit(embed=embed, view=view)
            else:
                embed = create_blackjack_embed(self.client, "**Player** wins", player_hand, dealer_hand)
                view = create_final_view()
                await interaction.message.edit(embed=embed, view=view)

        async def one_to_one_callback(interaction: Interaction):
            embed = create_blackjack_embed(self.client, "**Player** takes 1:1", player_hand, dealer_hand)
            view = create_final_view()
            await interaction.message.edit(embed=embed, view=view)

        if check_for_blackjack(player_hand):
            if str(dealer_hand.cards[1]) in maybe_blackjack_cards:
                dealer_blackjack = create_button("Blackjack", dealer_blackjack_callback, False)
                one_to_one = create_button("1:1", one_to_one_callback, False)
                view = View(timeout=180)
                view.add_item(dealer_blackjack)
                view.add_item(one_to_one)

                embed = create_game_start_blackjack_embed(self.client, f"turn {turn}", player_hand, dealer_hand)
                await interaction.followup.send(embed=embed, view=view)
            else:
                embed = create_blackjack_embed(self.client, "**Player** wins", player_hand, dealer_hand)
                view = create_final_view()
                await interaction.followup.send(embed=embed, view=view)
        else:
            if check_for_blackjack(dealer_hand):
                embed = create_blackjack_embed(self.client, "**Dealer** wins", player_hand, dealer_hand)
                view = create_final_view()
                await interaction.followup.send(embed=embed, view=view)
            else:
                hit = create_button("hit", hit_callback, False)
                stand = create_button("stand", stand_callback, False)
                view = View(timeout=180)
                view.add_item(hit)
                view.add_item(stand)

                embed = create_game_start_blackjack_embed(self.client, f"turn {turn}", player_hand, dealer_hand)
                await interaction.followup.send(embed=embed, view=view)

    @nextcord.slash_command(name='slots',
                            default_member_permissions=Permissions(send_messages=True))
    async def __slots(self, interaction: Interaction):
        player_got_row = spin_slots()
        is_win, multiplier = check_win_get_multiplier(player_got_row)
        if is_win is True:
            game_state = '**win**'
            embed = create_slots_embed(interaction.guild.id, interaction.user.id, interaction.user.display_avatar,
                                       interaction.application_command.name, player_got_row, game_state)
            await interaction.response.send_message(embed=embed)
        else:
            game_state = '**loose**'
            embed = create_slots_embed(interaction.guild.id, interaction.user.id, interaction.user.display_avatar,
                                       interaction.application_command.name, player_got_row, game_state)
            await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name='brick_knife_evidence_yandere',
                            default_member_permissions=Permissions(send_messages=True))
    async def __brick_knife_evidence_yandere_tentacles(self, interaction: Interaction):
        await interaction.response.defer()
        embed = create_starting_embed("Brick Knife Evidence Yandere Tentacles",
                                      "Pick 1 of 5 options and see that's will happen")
        view = create_starting_view()
        await interaction.followup.send(embed=embed, view=view)


def setup(client):
    client.add_cog(Games(client))
