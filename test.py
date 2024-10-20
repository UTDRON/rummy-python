from operator import truediv
from collections import Counter
# import numpy as np

def get_jokers(joker_card_rank):
    joker_cards = []
    suits = ["D","C","H","S"]
    for suit in suits:
        pass



def find_pure_sequences(cards):
    sequence_cards = []
    if 14 in cards and 2 in cards:
        sequence_cards.extend([14,2])
        for i in range(3,14):
            if i in cards:
                sequence_cards.append(i)
            else:
                if len(sequence_cards) >= 3:
                    print(sequence_cards)
                    print("LENGDI")
                    sequence_cards = []
                    break
                else:
                    sequence_cards = []
        sequence_cards = []
    for i in range(2,16):
        # sequence_cards.append(i)
        if i in cards:
            sequence_cards.append(i)
        else:
            if len(sequence_cards) >= 3:
                print(sequence_cards)
                # print("NON-LENGDI")
                # print(i)
            sequence_cards = []

def find_impure_sequences(cards):
    impure_seqence = []
    for i in range(2,14):
        if set([i,i+1]) <= set(cards):
            impure_seqence.append(i)
            impure_seqence.append(i+1)
            print(impure_seqence)
            impure_seqence = []
        elif i < 13 and set([i,i+2]) <= set(cards):
            impure_seqence.append(i)
            impure_seqence.append(i+2)
            print(impure_seqence)
            impure_seqence = []
    if set([14,2]) <=set(cards):
        impure_seqence.append(14)
        impure_seqence.append(2)
        print(impure_seqence)
        impure_seqence = []
    if set([14,3]) <=set(cards):
        impure_seqence.append(14)
        impure_seqence.append(3)
        print(impure_seqence)
        impure_seqence = []

# find_pure_sequences([2,3,5,8,9,12,13,14])

def fit_into_impure_sequence(imp_seq, card):
    pass


group1 = [['14♦', '3♦'], ['14♦', '3♦', '4♦'], ['3♦', '4♦'], ['3♦', '5♦'], ['4♦', '5♦']]
group2 =  [['4♣', '9♣'], ['4♣', '6♣', '7♣'], ['6♣', '7♣'], ['13♠', '14♠']]


def meld_sum(meld):
    sum = 0
    for item in meld:
        if int(item[:-1]) > 10:
            sum += 10
        else:
            sum += int(item[:-1])
    return sum

def sort_meld_groups(group):
    for i in range(len(group)): 
        swapped = False
        for j in range(0, len(group) - i - 1):
            if meld_sum(group[j]) < meld_sum(group[j + 1]):
                temp = group[j]
                group[j] = group[j+1]
                group[j+1] = temp
                swapped = True   
        if not swapped:
            break
    return group

# print(sort_meld_groups(group2))

# group1 = [['14♦', '3♦'], ['14♦', '3♦', '4♦'], ['3♦', '4♦'], ['3♦', '5♦'], ['4♦', '5♦']]
# group2 =  [['4♣', '9♣'], ['4♣', '6♣', '7♣'], ['6♣', '7♣'], ['13♠', '14♠']]

# group1 = set([str(a) for a in group1])
# print(group1)

def subtract_lists(a, b):
    multiset_difference = Counter(a) - Counter(b)
    result              = []
    for i in a:
        if i in multiset_difference:
            result.append(i)
            multiset_difference -= Counter((i,))
    return result

a = ['9♦', '9♠']  
b =['9♦', '9♠', '10♠']
print(subtract_lists(a,b))
a = []
if a:
    print("YES")

def chain_of_arranged_cards():
    #expand a tree, depth first
    cards = ["2♠", "3♠", "4♠", "5♠", "6♥", "7♠", "8♠", "9♠", "10♠", "11♠", "12♠", "13♠", "14♠", "15*"]
    wildcard = "15*"
    for card in cards:
        # find 
        pass
