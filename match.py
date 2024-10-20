from operator import mod
from time import sleep
from cards import *
from player import *
from utils import *
import random

game_play = True
# no_of_players = input(print("Enter No. of Players: "))
no_of_players = 2
# while game_play:
random.shuffle(deck)

#deal cards
for i in range(13):
    for j in range(no_of_players):
        players[j].cards.append(deck[i * no_of_players+j])

# print("AFTER ARRANGING")
for player in players:
    player.sorted_cards = sort_cards(player.cards)
    print(player.position, ":", end='')
    for i in range(len(player.sorted_cards)):
        print(player.sorted_cards[i].name, end=',')
    print("\n")
