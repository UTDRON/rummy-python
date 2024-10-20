import numpy as np
from cards import unshuffled_deck
from copy import deepcopy
import random
import player

spade = "♠"
heart = "♥"
diamond = "♦"
club = "♣"
joker = "*"

suits_letter = {
    "♦": 0,
    "♣": 1,
    "♥": 2,
    "♠": 3,
    "*": 4
}
suits = {
    0: "♦",
    1: "♣",
    2: "♥",
    3: "♠",
    4: "*"
}

'''
Create a 2d matrix that represents cards a player has, each element represents the no of that particular card
'''
def fill_cards_matrix(cards):
    matrix = np.zeros((5, 14) , dtype=np.int64)
    for card in cards:
        if card[-1] == "♦":
            matrix[0][int(card[:-1])-2] += 1
        elif card[-1] == "♣":
            matrix[1][int(card[:-1])-2] += 1
        elif card[-1] == "♥":
            matrix[2][int(card[:-1])-2] += 1
        elif card[-1] == "♠":
            matrix[3][int(card[:-1])-2] += 1
        else:
            matrix[4][int(card[:-1])-2] += 1
    return matrix

'''
Finds all possible pure sequences- of length 3,4 and 5
'''
def find_all_possible_pure_sequences(matrix):
    sequence_cards = []
    dummy_sequence = []
    #Backtrack and precompute ???
    for suit in range(4):
        sequence = []
        if matrix[suit][0] > 0 and matrix[suit][1] > 0 and matrix[suit][12] > 0:
            sequence.append(str(14)+suits[suit])
            sequence.append(str(2)+suits[suit])
            sequence.append(str(3)+suits[suit])
            dummy_sequence = deepcopy(sequence)
            sequence_cards.append(dummy_sequence)
            dummy_sequence = []
            if matrix[suit][2] > 0:
                sequence.append(str(4)+suits[suit])
                dummy_sequence = deepcopy(sequence)
                sequence_cards.append(dummy_sequence)
                dummy_sequence = []
                if matrix[suit][3] > 0:
                    sequence.append(str(5)+suits[suit])
                    dummy_sequence = deepcopy(sequence)
                    sequence_cards.append(dummy_sequence)
        if sequence:
            sequence = []
        for rank in range(11):
            if matrix[suit][rank] > 0:
                if matrix[suit][rank + 1] > 0  and matrix[suit][rank + 2] > 0:
                    sequence.append(str(rank + 2)+suits[suit])
                    sequence.append(str(rank + 3)+suits[suit])
                    sequence.append(str(rank + 4)+suits[suit])
                    dummy_sequence = deepcopy(sequence)
                    sequence_cards.append(dummy_sequence)
                    dummy_sequence = []
                    if matrix[suit][rank + 3] > 0:
                        sequence.append(str(rank + 5)+suits[suit])
                        dummy_sequence = deepcopy(sequence)
                        sequence_cards.append(dummy_sequence)
                        dummy_sequence = []
                        if matrix[suit][rank + 4] > 0:
                            sequence.append(str(rank + 6)+suits[suit])
                            dummy_sequence = deepcopy(sequence)
                            sequence_cards.append(dummy_sequence)
                sequence = []
            else:
                continue
    return sequence_cards

'''
Finds all possible incomplete sequence houses
'''
def find_all_possible_incomplete_sequences(matrix):
    sequence_houses = []
    for suit in range(4):
        house = []
        dummy_house = []
        if matrix[suit][12] > 0:
            if matrix[suit][0] > 0:
                house.append(str(14)+suits[suit])
                house.append(str(2)+suits[suit])
                dummy_house = deepcopy(house)
                sequence_houses.append(dummy_house)
                dummy_house = []
                if matrix[suit][2] > 0:
                    house.append(str(4)+suits[suit])
                    dummy_house = deepcopy(house)
                    sequence_houses.append(dummy_house)
                    dummy_house = []
                    if matrix[suit][3] > 0:
                        house.append(str(5)+suits[suit])
                        dummy_house = deepcopy(house)
                        sequence_houses.append(dummy_house)
                        dummy_house = []
            if house:   
                house = []

            if matrix[suit][1] > 0:
                house.append(str(14)+suits[suit])
                house.append(str(3)+suits[suit])
                dummy_house = deepcopy(house)
                sequence_houses.append(dummy_house)
                dummy_house = []
                if matrix[suit][2] > 0:
                    house.append(str(4)+suits[suit])
                    dummy_house = deepcopy(house)
                    sequence_houses.append(dummy_house)
                    dummy_house = []

        if house:   
            house = []
        for rank in range(12):
            if matrix[suit][rank] > 0 and matrix[suit][rank + 1] > 0:
                house.append(str(rank + 2)+suits[suit])
                house.append(str(rank + 3)+suits[suit])
                dummy_house = deepcopy(house)
                sequence_houses.append(dummy_house)
                dummy_house = []
                if rank < 10:
                    if matrix[suit][rank + 3] > 0:
                        house.append(str(rank + 5)+suits[suit])
                        dummy_house = deepcopy(house)
                        sequence_houses.append(dummy_house)
                        dummy_house = []
                        if rank < 9:
                            if matrix[suit][rank + 4] > 0:
                                house.append(str(rank + 6)+suits[suit])
                                dummy_house = deepcopy(house)
                                sequence_houses.append(dummy_house)
                                dummy_house = []
            
            if house:   
                house = []

            if matrix[suit][rank] > 0 and matrix[suit][rank + 2] > 0 and rank < 11:
                house.append(str(rank + 2)+suits[suit])
                house.append(str(rank + 4)+suits[suit])
                dummy_house = deepcopy(house)
                sequence_houses.append(dummy_house)
                dummy_house = []
                if rank < 10:
                    if matrix[suit][rank + 3] > 0:
                        house.append(str(rank + 5)+suits[suit])
                        dummy_house = deepcopy(house)
                        sequence_houses.append(dummy_house)
                        dummy_house = []
            house = []

    return sequence_houses

'''
Finds all possible complete sets of length 3 & 4 from your cards
'''
def find_all_possible_complete_sets(matrix):
    sets_cards = []
    for rank in range(13):
        sets = []
        for suit in range(4):
            if matrix[suit][rank] > 0:
                sets.append(str(rank + 2)+suits[suit])
        if len(sets) >= 3:
            sets_cards.append(sets)
        if len(sets) == 4:
            sets = []
            sets.append(str(rank + 2)+suits[0])
            sets.append(str(rank + 2)+suits[1])
            sets.append(str(rank + 2)+suits[2])
            sets_cards.append(sets)
            sets = []
            sets.append(str(rank + 2)+suits[0])
            sets.append(str(rank + 2)+suits[1])
            sets.append(str(rank + 2)+suits[3])
            sets_cards.append(sets)
            sets = []
            sets.append(str(rank + 2)+suits[0])
            sets.append(str(rank + 2)+suits[2])
            sets.append(str(rank + 2)+suits[3])
            sets_cards.append(sets)
            sets = []
            sets.append(str(rank + 2)+suits[1])
            sets.append(str(rank + 2)+suits[2])
            sets.append(str(rank + 2)+suits[3])
            sets_cards.append(sets)

    return sets_cards

'''
Finds all possible incomplete sets of length 2
'''
def find_all_possible_sets_houses(matrix):
    sets_houses = []
    for rank in range(13):
        house = []
        for suit in range(4):
            for next_suit in range(suit+1, 4):
                if matrix[suit][rank] > 0 and matrix[next_suit][rank] > 0:
                    house.append(str(rank + 2)+suits[suit])
                    house.append(str(rank + 2)+suits[next_suit])
                    sets_houses.append(house)
                    house = []
    return sets_houses

'''
Finds all possible incomplete sequence houses with 2 successive cards missing
'''
def find_all_possible_two_break_sequence_houses(matrix):
    seq_houses = []
    for suit in range(4):
        house = []
        dummy_house = []
        if matrix[suit][12] > 0 and matrix[suit][2] > 0:
            house.append(str(14)+suits[suit])
            house.append(str(4)+suits[suit])
            dummy_house = deepcopy(house)
            seq_houses.append(dummy_house)
        
        if house:   
            house = []
            
        for rank in range(10):
            if matrix[suit][rank] > 0 and matrix[suit][rank + 3] > 0:
                house.append(str(rank + 2)+suits[suit])
                house.append(str(rank + 5)+suits[suit])
                dummy_house = deepcopy(house)
                seq_houses.append(dummy_house)
                dummy_house = []
            if house:   
                house = []
                
    return seq_houses

'''
Evaluates all the cards that do not fall in any melds
'''
def find_all_extra_cards(matrix):
    extra_cards = []
    for rank in range(13):
        for suit in range(4):
            if matrix[suit][rank] > 0:
                extra_cards.append(str(rank+2)+suits[suit])
    return extra_cards

'''
Displays cards sorted based on suits and ranks
'''
def display_sorted_cards():
    all_cards = []
    for suit in range(5):
        suit_cards = []
        for rank in range(14):
            if cards_matrix[suit][rank] == 1:
                suit_cards.append(str(rank+2)+suits[suit])
            elif cards_matrix[suit][rank] == 2:
                suit_cards.append(str(rank+2)+suits[suit])
                suit_cards.append(str(rank+2)+suits[suit])
        all_cards.append(suit_cards)
    return all_cards

'''
Evaluates all wildcards and jokers a player owns
'''
def get_wildcards(cards):
    my_wildcards = []
    if wildcard == '15*':
        for card in cards:
            if card[:-1] == '14':
                my_wildcards.append(card)
            if card == '15*':
                my_wildcards.append(card)
    else:
        for card in cards:
            if card[:-1] == wildcard[:-1]:
                my_wildcards.append(card)
            if card == '15*':
                my_wildcards.append(card)
    return my_wildcards

'''
Removes wildcards and jokers from cards matrix
'''
def get_cards_matrix_without_wildcards(cards):
    cards_matrix_without_wildcards = []
    cards_matrix_without_wildcards = deepcopy(cards_matrix)
    wildcards = get_wildcards(cards) 
    if wildcards:
        for card in get_wildcards(cards):
            cards_matrix_without_wildcards[int(suits_letter[card[-1]])][int(card[:-1]) - 2] -= 1
    return cards_matrix_without_wildcards


# cards = ["2♠", "3♠", "4♠", "5♠", "6♥", "7♠", "8♠", "9♠", "10♠", "11♠", "12♠", "13♠", "14♠", "15*"]
# wildcard = "15*"

# cards = ["11♦",	"12♦",	"13♦",	"4♠",	"3♠",	"14♠",	"6♣",	"4♥",	"3♥",	"5♦",	"6♦",	"6♠",	"8♦"]
# wildcard = "6♠"

# cards = ['14♠', '10♣', '11♠', '12♣', '9♥', '7♦', '11♥', '3♣', '2♣', '12♠', '7♣', '9♣', '5♦', '4♦']
# wildcard = '13♥'

cards = []
wildcard = None
random.shuffle(unshuffled_deck)

for i in range(len(unshuffled_deck)):
    cards.append(unshuffled_deck[i])
    if len(cards) ==  14:
        wildcard = unshuffled_deck[i+1]
        break


# cards_matrix = np.zeros((5, 14) , dtype=np.int64)
print("MY CARDS: ",cards)
cards_matrix = fill_cards_matrix(cards)
print(cards_matrix)
cards_matrix_without_wildcards = get_cards_matrix_without_wildcards(cards)

print("SORTED CARDS: ",display_sorted_cards())
print("WILDCARD: ",wildcard)

pure_sequences = find_all_possible_pure_sequences(cards_matrix)
pure_sequences_without_wildcards = find_all_possible_pure_sequences(cards_matrix_without_wildcards)

incomplete_sequences_houses = find_all_possible_incomplete_sequences(cards_matrix)
incomplete_sequences_houses_without_wildcards = find_all_possible_incomplete_sequences(cards_matrix_without_wildcards)

two_break_sequences_houses = find_all_possible_two_break_sequence_houses(cards_matrix)
two_break_sequences_houses_without_wildcards = find_all_possible_two_break_sequence_houses(cards_matrix_without_wildcards)

complete_sets = find_all_possible_complete_sets(cards_matrix)
complete_sets_without_wildcards = find_all_possible_complete_sets(cards_matrix_without_wildcards)

incomplete_sets_houses = find_all_possible_sets_houses(cards_matrix)
incomplete_sets_houses_without_wildcards = find_all_possible_sets_houses(cards_matrix_without_wildcards)

incomplete_sequences_and_sets = incomplete_sequences_houses + incomplete_sets_houses
incomplete_sequences_and_sets_without_wildcards = incomplete_sequences_houses_without_wildcards + incomplete_sets_houses_without_wildcards

print("Possible Pure Sequences:",pure_sequences)
print("Possible Pure Sequences Without Wildcards:",pure_sequences_without_wildcards)

print("Possible Incomplete Sequences Houses:",incomplete_sequences_houses)
print("Possible Incomplete Sequences Houses Without Wildcards:",incomplete_sequences_houses_without_wildcards)


print("Two Break Sequence Houses:",two_break_sequences_houses)
print("Two Break Sequence Houses Without Wildcards:",two_break_sequences_houses_without_wildcards)

print("Possible Complete Sets:",complete_sets)
print("Possible Complete Sets Without Wildcards:",complete_sets_without_wildcards)

print("Possible Incomplete Sets Houses:",incomplete_sets_houses)
print("Possible Incomplete Sets Houses Without Wildcards:",incomplete_sets_houses_without_wildcards)

print("Possible Incomplete Sequences and Sets: ",incomplete_sequences_and_sets )
print("Possible Incomplete Sequences and Sets Without Wildcards: ",incomplete_sequences_and_sets_without_wildcards)

updated_cards_matrix = deepcopy(cards_matrix)
