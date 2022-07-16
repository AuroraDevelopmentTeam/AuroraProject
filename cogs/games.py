import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle, File
from nextcord.ui import Button, View

from core.games.blackjack import Hand, Deck, check_for_blackjack, show_blackjack_results, player_is_over


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="blackjack", description="play blackjack game")
    async def __blackjack(self, interaction: Interaction):
        await interaction.response.defer()
        deck = Deck()
        deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand(dealer=True)
        turn = 1

        for i in range(2):
            player_hand.add_card(deck.deal())
            dealer_hand.add_card(deck.deal())

        hit = Button(label="click me", style=ButtonStyle.blurple)

        async def hit_callback(interaction):
            print('hit button pressed')

        embed = nextcord.Embed(title=interaction.application_command.name,
                               description=f'turn: {turn}\nplayer_hand: {player_hand.cards} value {player_hand.get_value()}\n dealer_hand: {dealer_hand.display()}')
        msg = await interaction.followup.send(embed=embed)

        game_over = False

        while not game_over:
            if turn == 1:
                player_has_blackjack, dealer_has_blackjack = check_for_blackjack(player_hand, dealer_hand)
                if player_has_blackjack or dealer_has_blackjack:
                    game_over = True
                    show_blackjack_results(
                        player_has_blackjack, dealer_has_blackjack)
                    description = f'turn: {turn}\nblackjack!\ndealer_hand: {dealer_hand.cards} value ' \
                                  f'{dealer_hand.get_value()}\nplayer_hand: {player_hand.cards} value ' \
                                  f'{player_hand.get_value()} '
                    embed = nextcord.Embed(title=interaction.application_command.name, description=description)
                    await msg.edit(embed=embed)
                    continue
            await interaction.channel.send('write h/s')

            def check(message):
                return message.content.casefold() in (
                    'h', 's', 'hit', 'stick')

            reply = await self.client.wait_for('message', check=check, timeout=180)
            if reply.content.casefold() == 'h':
                turn += 1
                player_hand.add_card(deck.deal())
                description = f'turn: {turn}\nplayer_hand: {player_hand.cards}, dealer_hand: {dealer_hand.display()}'
                embed = nextcord.Embed(title=interaction.application_command.name, description=description)
                await msg.edit(embed=embed)
                if player_is_over(player_hand):
                    description = f'turn: {turn}\ndealer wins!\ndealer_hand: {dealer_hand.cards} value {dealer_hand.get_value()}\nplayer_hand: {player_hand.cards} value {player_hand.get_value()}'
                    embed = nextcord.Embed(title=interaction.application_command.name, description=description)
                    await msg.edit(embed=embed)

            if reply.content.casefold() == 's':
                turn += 1
                while dealer_hand.get_value() < 17:
                    dealer_hand.add_card(deck.deal())
                    if player_is_over(dealer_hand):
                        description = f'turn: {turn}\nplayer wins!\ndealer_hand: {dealer_hand.cards} value {dealer_hand.get_value()}\nplayer_hand: {player_hand.cards} value {player_hand.get_value()}'
                        embed = nextcord.Embed(title=interaction.application_command.name, description=description)
                        await msg.edit(embed=embed)
                if not player_is_over(dealer_hand):
                    if dealer_hand.get_value() > player_hand.get_value():
                        description = f'turn: {turn}\ndealer wins\ndealer_hand: {dealer_hand.cards} value {dealer_hand.get_value()}\nplayer_hand: {player_hand.cards} value {player_hand.get_value()}'
                        embed = nextcord.Embed(title=interaction.application_command.name, description=description)
                        await msg.edit(embed=embed)
                        game_over = True
                    elif dealer_hand.get_value() == player_hand.get_value():
                        description = f'turn: {turn}\ndraw!\ndealer_hand: {dealer_hand.cards} value {dealer_hand.get_value()}\nplayer_hand: {player_hand.cards} value {player_hand.get_value()}'
                        embed = nextcord.Embed(title=interaction.application_command.name, description=description)
                        await msg.edit(embed=embed)
                        game_over = True
                    else:
                        description = f'turn: {turn}\nplayer wins!\ndealer_hand: {dealer_hand.cards} value {dealer_hand.get_value()}\nplayer_hand: {player_hand.cards} value {player_hand.get_value()}'
                        embed = nextcord.Embed(title=interaction.application_command.name, description=description)
                        await msg.edit(embed=embed)
                        game_over = True


def setup(client):
    client.add_cog(Games(client))
