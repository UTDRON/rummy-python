class Card:
    def __init__(self,rank, suit):
        self.name = str(rank)+str(suit)
        self.rank = rank
        self.suit = suit
        self.owner = None


spade = "♠"
heart = "♥"
diamond = "♦"
club = "♣"
suits = ["♦","♣","♥","♠"]
ranks = [2,3,4,5,6,7,8,9,10,11,12,13,14]
deck = []
# for suit in suits:
#     for rank in ranks:
#         card = Card(rank,suit)
#         deck.append(card)
#         deck.append(card)
for suit in suits:
    for rank in ranks:
        card = str(rank)+suit
        deck.append(card)
        deck.append(card)
deck.append('15*')
deck.append('15*')

unshuffled_deck = list(deck)