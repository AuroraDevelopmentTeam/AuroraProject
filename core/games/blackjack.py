import random


cards_emoji_representation = {
    "hidden": 998155897543082064,
    "A of Diamonds": 997331027888451695,
    "2 of Diamonds": 997331048545402880,
    "3 of Diamonds": 997331053620494387,
    "4 of Diamonds": 997331044686635051,
    "5 of Diamonds": 997331043403190302,
    "6 of Diamonds": 997331050252472383,
    "7 of Diamonds": 997331041595424868,
    "8 of Diamonds": 997331037157867560,
    "9 of Diamonds": 997331038609084517,
    "10 of Diamonds": 997331040060330054,
    "J of Diamonds": 997331033462677546,
    "Q of Diamonds": 997331031000621088,
    "K of Diamonds": 997331029364850688,
    "A of Clubs": 997331010935070801,
    "2 of Clubs": 997331020896546879,
    "3 of Clubs": 997331024369430548,
    "4 of Clubs": 997331026059722802,
    "5 of Clubs": 997331019285942422,
    "6 of Clubs": 997331014072414308,
    "7 of Clubs": 997331008045191179,
    "8 of Clubs": 997331022582644826,
    "9 of Clubs": 998158745760698419,
    "10 of Clubs": 997331012562456606,
    "J of Clubs": 997331015049682985,
    "Q of Clubs": 997331009534169088,
    "K of Clubs": 997331017151025234,
    "A of Spades": 998165414121062400,
    "2 of Spades": 998165411768053783,
    "3 of Spades": 998165422702592040,
    "4 of Spades": 998165419640754287,
    "5 of Spades": 998165959921631294,
    "6 of Spades": 998165417006731264,
    "7 of Spades": 998165429484781669,
    "8 of Spades": 998165424652951562,
    "9 of Spades": 998165415098327051,
    "10 of Spades": 998165418298580992,
    "J of Spades": 998165420932595723,
    "Q of Spades": 998165426125152307,
    "K of Spades": 998165427563790403,
    "A of Hearts": 998173493067784203,
    "2 of Hearts": 998173478119280680,
    "3 of Hearts": 998173481269203054,
    "4 of Hearts": 998173479444680765,
    "5 of Hearts": 998173482535887010,
    "6 of Hearts": 998173494766473226,
    "7 of Hearts": 998173491566235679,
    "8 of Hearts": 998173497530515587,
    "9 of Hearts": 998173484729512028,
    "10 of Hearts": 998173496117043251,
    "J of Hearts": 998173486981857450,
    "Q of Hearts": 998173489037066353,
    "K of Hearts": 998173490345680978
}


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
        self.cards = [Card(s, v) for s in ["Clubs", "Spades", "Hearts",
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
