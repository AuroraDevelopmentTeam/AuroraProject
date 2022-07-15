import random


def check_for_blackjack(player_hand, dealer_hand):
    player = False
    dealer = False
    if player_hand.get_value() == 21:
        player = True
    if dealer_hand.get_value() == 21:
        dealer = True

    return player, dealer


def player_is_over(player_hand):
    return player_hand.get_value() > 21


def show_blackjack_results(player_has_blackjack, dealer_has_blackjack):
    if player_has_blackjack and dealer_has_blackjack:
        print("Both players have blackjack! Draw!")

    elif player_has_blackjack:
        print("You have blackjack! You win!")

    elif dealer_has_blackjack:
        print("Dealer has blackjack! Dealer wins!")


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return " of ".join((self.value, self.suit))


class Deck:
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts",
                                           "Diamonds"] for v in ["A", "2", "3", "4", "5", "6",
                                                                 "7", "8", "9", "10", "J", "Q", "K"]]

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)


class Hand:
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    has_ace = True
                    self.value += 11
                else:
                    self.value += 10

        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value

    def display(self):
        if self.dealer:
            return ["hidden", self.cards[1]]
        else:
            for card in self.cards:
                print(card)
            print(self.get_value())
