from copy import deepcopy

def find_all_possible_pure_sequences(cards):
    sequence_cards = []
    dummy_sequence = []
    for rank in cards:
        sequence = []
        if rank == 14 and 2 in cards and 3 in cards:
            sequence.append(14)
            sequence.append(2)
            sequence.append(3)
            dummy_sequence = deepcopy(sequence)
            sequence_cards.append(dummy_sequence)
            dummy_sequence = []
            if 4 in cards:
                sequence.append(4)
                dummy_sequence = deepcopy(sequence)
                sequence_cards.append(dummy_sequence)
                dummy_sequence = []
                if 5 in cards:
                    sequence.append(5)
                    dummy_sequence = deepcopy(sequence)
                    sequence_cards.append(dummy_sequence)
    
        if rank+1 in cards and rank+2 in cards:
            sequence.append(rank)
            sequence.append(rank + 1)
            sequence.append(rank + 2)
            dummy_sequence = deepcopy(sequence)
            sequence_cards.append(dummy_sequence)
            dummy_sequence = []
            if rank+3 in cards:
                sequence.append(rank + 3)
                dummy_sequence = deepcopy(sequence)
                sequence_cards.append(dummy_sequence)
                dummy_sequence = []
                if rank+4 in cards:
                    sequence.append(rank + 4)
                    dummy_sequence = deepcopy(sequence)
                    sequence_cards.append(dummy_sequence)
    return sequence_cards

def find_all_possible_incomplete_sequences(cards):
    sequence_houses = []
    #Backtrack and precompute
    for rank in cards:
        house = []
        dummy_house = []
        if rank == 14:
            if 2 in cards:
                house.append(14)
                house.append(2)
                dummy_house = deepcopy(house)
                sequence_houses.append(dummy_house)
                dummy_house = []
                if 4 in cards:
                    house.append(4)
                    dummy_house = deepcopy(house)
                    sequence_houses.append(dummy_house)
                    dummy_house = []
                    if 5 in cards:
                        house.append(5)
                        dummy_house = deepcopy(house)
                        sequence_houses.append(dummy_house)
                        dummy_house = []
            
            if house:   
                house = []

            if 3 in cards:
                house.append(14)
                house.append(3)
                dummy_house = deepcopy(house)
                sequence_houses.append(dummy_house)
                dummy_house = []
                if 4 in cards:
                    house.append(4)
                    dummy_house = deepcopy(house)
                    sequence_houses.append(dummy_house)
                    dummy_house = []
        
        if rank+1 in cards:
            house.append(rank)
            house.append(rank + 1)
            dummy_house = deepcopy(house)
            sequence_houses.append(dummy_house)
            dummy_house = []
            if rank+3 in cards:
                house.append(rank+3)
                dummy_house = deepcopy(house)
                sequence_houses.append(dummy_house)
                dummy_house = []
                if rank+4 in cards:
                    house.append(rank+4)
                    dummy_house = deepcopy(house)
                    sequence_houses.append(dummy_house)
                    dummy_house = []

        if house:   
            house = []

        if rank+2 in cards:
            house.append(rank)
            house.append(rank + 2)
            dummy_house = deepcopy(house)
            sequence_houses.append(dummy_house)
            dummy_house = []
            if rank+3 in cards:
                house.append(rank+3)
                dummy_house = deepcopy(house)
                sequence_houses.append(dummy_house)
                dummy_house = []
    return sequence_houses


cards = [3,8,12,13,14]
# print(find_all_possible_pure_sequences(cards))
print(find_all_possible_incomplete_sequences(cards))