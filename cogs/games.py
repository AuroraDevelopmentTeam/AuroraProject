import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle, File
from nextcord.ui import Button, View

from core.games.blackjack import Hand, Deck, check_for_blackjack, show_blackjack_results, player_is_over, \
    cards_emoji_representation


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
        global turn
        turn = 1

        for i in range(2):
            player_hand.add_card(deck.deal())
            dealer_hand.add_card(deck.deal())

        hit = Button(label="hit", style=ButtonStyle.blurple)
        stand = Button(label="stand", style=ButtonStyle.blurple)

        async def hit_callback(interaction: Interaction):
            global turn
            turn += 1
            player_hand.add_card(deck.deal())
            if player_is_over(player_hand):
                embed = nextcord.Embed(title='Blackjack', description='**Dealer** wins')
                player_hand_field_value = ' '
                dealer_hand_field_value = ' '
                for card in player_hand.cards:
                    card = str(card)
                    if card in cards_emoji_representation:
                        player_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                    else:
                        player_hand_field_value += f'{card} '
                embed.add_field(name='Player hand',
                                value=f'{player_hand_field_value}\nvalue **{player_hand.get_value()}**', inline=True)
                for card in dealer_hand.cards:
                    card = str(card)
                    if card in cards_emoji_representation:
                        dealer_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                    else:
                        dealer_hand_field_value += f'{card} '
                embed.add_field(name='Dealer hand', value=f'{dealer_hand_field_value}\nvalue **{dealer_hand.get_value()}**', inline=True)
                hit = Button(label="hit", style=ButtonStyle.blurple, disabled=True)
                stand = Button(label="stand", style=ButtonStyle.blurple, disabled=True)
                myview = View(timeout=180)
                myview.add_item(hit)
                myview.add_item(stand)
                await interaction.message.edit(embed=embed, view=myview)
            else:
                embed = nextcord.Embed(title='Blackjack', description=f'turn: {turn}')
                player_hand_field_value = ' '
                dealer_hand_field_value = ' '
                for card in player_hand.cards:
                    card = str(card)
                    if card in cards_emoji_representation:
                        player_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                    else:
                        player_hand_field_value += f'{card} '
                embed.add_field(name='Player hand',
                                value=f'{player_hand_field_value}\nvalue **{player_hand.get_value()}**', inline=True)
                for card in dealer_hand.display():
                    card = str(card)
                    if card in cards_emoji_representation:
                        dealer_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                    else:
                        dealer_hand_field_value += f'{card} '
                embed.add_field(name='Dealer hand',
                                value=f'{dealer_hand_field_value}', inline=True)
                await interaction.message.edit(embed=embed)

        async def stand_callback(interaction: Interaction):
            global turn
            turn += 1
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal())
                if player_is_over(dealer_hand):
                    embed = nextcord.Embed(title='Blackjack', description='**Player** wins')
                    player_hand_field_value = ' '
                    dealer_hand_field_value = ' '
                    for card in player_hand.cards:
                        card = str(card)
                        if card in cards_emoji_representation:
                            player_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                        else:
                            player_hand_field_value += f'{card} '
                    embed.add_field(name='Player hand',
                                    value=f'{player_hand_field_value}\nvalue **{player_hand.get_value()}**',
                                    inline=True)
                    for card in dealer_hand.cards:
                        card = str(card)
                        if card in cards_emoji_representation:
                            dealer_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                        else:
                            dealer_hand_field_value += f'{card} '
                    embed.add_field(name='Dealer hand',
                                    value=f'{dealer_hand_field_value}\nvalue **{dealer_hand.get_value()}**', inline=True)
                    hit = Button(label="hit", style=ButtonStyle.blurple, disabled=True)
                    stand = Button(label="stand", style=ButtonStyle.blurple, disabled=True)
                    myview = View(timeout=180)
                    myview.add_item(hit)
                    myview.add_item(stand)
                    await interaction.message.edit(embed=embed, view=myview)
            if 17 <= dealer_hand.get_value() <= 21:
                if dealer_hand.get_value() > player_hand.get_value():
                    embed = nextcord.Embed(title='Blackjack', description='**Dealer** wins')
                    player_hand_field_value = ' '
                    dealer_hand_field_value = ' '
                    for card in player_hand.cards:
                        card = str(card)
                        if card in cards_emoji_representation:
                            player_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                        else:
                            player_hand_field_value += f'{card} '
                    embed.add_field(name='Player hand',
                                    value=f'{player_hand_field_value}\nvalue **{player_hand.get_value()}**',
                                    inline=True)
                    for card in dealer_hand.cards:
                        card = str(card)
                        if card in cards_emoji_representation:
                            dealer_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                        else:
                            dealer_hand_field_value += f'{card} '
                    embed.add_field(name='Dealer hand',
                                    value=f'{dealer_hand_field_value}\nvalue **{dealer_hand.get_value()}**', inline=True)
                    hit = Button(label="hit", style=ButtonStyle.blurple, disabled=True)
                    stand = Button(label="stand", style=ButtonStyle.blurple, disabled=True)
                    myview = View(timeout=180)
                    myview.add_item(hit)
                    myview.add_item(stand)
                    await interaction.message.edit(embed=embed, view=myview)
                elif dealer_hand.get_value() == player_hand.get_value():
                    embed = nextcord.Embed(title='Blackjack', description='**Draw**')
                    player_hand_field_value = ' '
                    dealer_hand_field_value = ' '
                    for card in player_hand.cards:
                        card = str(card)
                        if card in cards_emoji_representation:
                            player_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                        else:
                            player_hand_field_value += f'{card} '
                    embed.add_field(name='Player hand',
                                    value=f'{player_hand_field_value}\nvalue **{player_hand.get_value()}**',
                                    inline=True)
                    for card in dealer_hand.cards:
                        card = str(card)
                        if card in cards_emoji_representation:
                            dealer_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                        else:
                            dealer_hand_field_value += f'{card} '
                    embed.add_field(name='Dealer hand',
                                    value=f'{dealer_hand_field_value}\nvalue **{dealer_hand.get_value()}**', inline=True)
                    hit = Button(label="hit", style=ButtonStyle.blurple, disabled=True)
                    stand = Button(label="stand", style=ButtonStyle.blurple, disabled=True)
                    myview = View(timeout=180)
                    myview.add_item(hit)
                    myview.add_item(stand)
                    await interaction.message.edit(embed=embed, view=myview)
                else:
                    embed = nextcord.Embed(title='Blackjack', description='**Player** wins')
                    player_hand_field_value = ' '
                    dealer_hand_field_value = ' '
                    for card in player_hand.cards:
                        card = str(card)
                        if card in cards_emoji_representation:
                            player_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                        else:
                            player_hand_field_value += f'{card} '
                    embed.add_field(name='Player hand',
                                    value=f'{player_hand_field_value}\nvalue **{player_hand.get_value()}**',
                                    inline=True)
                    for card in dealer_hand.cards:
                        card = str(card)
                        if card in cards_emoji_representation:
                            dealer_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
                        else:
                            dealer_hand_field_value += f'{card} '
                    embed.add_field(name='Dealer hand',
                                    value=f'{dealer_hand_field_value}\nvalue **{dealer_hand.get_value()}**', inline=True)
                    hit = Button(label="hit", style=ButtonStyle.blurple, disabled=True)
                    stand = Button(label="stand", style=ButtonStyle.blurple, disabled=True)
                    myview = View(timeout=180)
                    myview.add_item(hit)
                    myview.add_item(stand)
                    await interaction.message.edit(embed=embed, view=myview)

        hit.callback = hit_callback
        stand.callback = stand_callback

        game_over = False

        myview = View(timeout=180)
        myview.add_item(hit)
        myview.add_item(stand)

        embed = nextcord.Embed(title='Blackjack', description=f'turn {turn}')
        player_hand_field_value = ''
        dealer_hand_field_value = ''
        for card in player_hand.cards:
            card = str(card)
            if card in cards_emoji_representation:
                player_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
            else:
                player_hand_field_value += f'{card} '
        embed.add_field(name='Player hand',
                        value=f'{player_hand_field_value}\nvalue **{player_hand.get_value()}**', inline=True)
        for card in dealer_hand.display():
            card = str(card)
            if card in cards_emoji_representation:
                dealer_hand_field_value += f'{self.client.get_emoji(cards_emoji_representation[card])} '
            else:
                dealer_hand_field_value += f'{card} '
        embed.add_field(name='Dealer hand',
                        value=f'{dealer_hand_field_value}', inline=True)
        msg = await interaction.followup.send(embed=embed, view=myview)


def setup(client):
    client.add_cog(Games(client))
