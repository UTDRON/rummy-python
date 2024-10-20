from pile import *
from cards import deck

def sort_cards(cards):
    arranged_cards = []
    for suit in ["D","C","H","S"]:
        suit_cards = []
        for card in cards:
            if card.suit == suit:
                suit_cards.append(card.rank)
        suit_cards.sort()
        for card in suit_cards:
            for card_obj in cards:
                if str(card)+suit == card_obj.name:
                    arranged_cards.append(card_obj)
    return arranged_cards

def find_pure_sequence(cards):
    pass

def validate_pure_sequence():
    pass

def validate_impure_sequence():
    pass

def validate_pure_set():
    pass

def validate_impure_set():
    pass

def evaluate_jokers():
    pass

def validate_first_life():
    pass

def validate_second_life():
    pass

def validate_third_group():
    pass

def validate_fourth_group():
    pass

def validate_show():
    validate_first_life()
    validate_second_life()
    validate_third_group()
    validate_fourth_group()
    pass

def get_four_cards_group():
    pass

def update_cards_on_pile(discarded_card):
    pile.cards.append(discarded_card)
    pass

def get_remaining_cards(player):
    return list(set(deck)-set(pile)-set(player.cards))




