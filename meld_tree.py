from time import time
from cards_matrix import *
from collections import Counter
import numpy as np

class TreeNode:
    '''
    Defining Fields of a Tree Node
    Each node represents a combination of cards or a "MELD"
    '''
    def __init__(self, data):
        self.data                                   = data
        self.children                               = []
        self.updated_cards_matrix                   = [[]]
        self.updated_cards_matrix_without_wildcards = [[]]
        self.parent                                 = None
        self.level                                  = None
        self.reward                                 = 0
        self.reward_sum                             = 0
        self.cards_until_now                        = []
        self.melds_until_now                        = []
        self.used_wildcard                          = []
        self.used_wildcards_until_now               = []

    '''
    Returns the level of a node in tree hierarchy
    '''
    def get_level(self):
        level       = 0
        p           = self.parent

        while p:
            level   += 1
            p       = p.parent

        return level
    
    '''
    Returns children of sibling/cousin nodes or nodes on same level as me
    '''
    def get_nephews(self):
        nephews = []
        for node in all_nodes_list:
            if node != self and node.level == self.level + 1 and node.parent != self:
                nephews.append(node)
        return nephews
    
    '''
    Returns sibling and their children
    '''
    def get_sibling_nephew_pair(self):
        sibling_nephew_pair = []
        for node in all_nodes_list:
            if node != self and node.level == self.level:
                for child in node.children:
                    pair = []
                    pair.append(node.data)
                    pair.append(child.data)
                    sibling_nephew_pair.append(pair)
        return sibling_nephew_pair
    
    '''
    Displays Tree View of Nodes in Hierarchy
    '''
    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + str(self.data) ," Reward: ", self.reward, " Reward Sum: ", \
            self.reward_sum, " Used Wildcard: ", self.used_wildcard," Used Wildcards Until Now: ", \
            self.used_wildcards_until_now)
        # print(prefix + str(self.data))
        if self.children:
            for child in self.children:
                child.print_tree()

    '''
    Adds children to a node
    '''
    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    '''
    Removes used cards from cards matrix
    '''
    def get_updated_cards_matrix(self,cards,matrix):
        self.updated_cards_matrix = deepcopy(matrix)
        for card in cards:
            self.updated_cards_matrix[int(suits_letter[card[-1]])][int(card[:-1]) - 2] -= 1

class Melds:
    '''
    Defining Fields for card melds groups
    '''
    def __init__(self, data):
        self.data                                   = deepcopy(data)
        self.first_life                             = self.is_first_life()
        self.second_life                            = self.is_second_life()
        self.reward_sum                             = self.get_reward_sum()
        self.throw_card                             = None
        self.data                                   = self.fill_data()
    
    '''
    Returns if combination has first life or pure sequence
    '''
    def is_first_life(self):
        if self.data[-1].reward_sum == 0:
            return True
        return False
    
    '''
    Returns if combination has second life or pure/impure sequence
    '''
    def is_second_life(self):
        if self.is_first_life():
            for i in range(len(self.data)-1):
                if self.data[i].reward == 0:
                    return True
        return False
    
    '''
    Returns total sum of cards from cards melds group
    '''
    def get_reward_sum(self):
        return self.data[0].reward_sum

    def fill_data(self):
        i = len(self.data)-1
        while i >= 0:
            if self.data[i].data in pure_sequences:
                pass

            elif self.data[i].data == []:
                if get_used_wildcard(self.data[i]) not in self.data[i].data:
                    self.data[i].data.extend(get_used_wildcard(self.data[i]))
                if get_highest_ranked_card(self.data[0].data) not in self.data[i].data:
                    attach_card = get_highest_ranked_card(self.data[0].data)
                    self.data[i].data.extend(attach_card)
                    self.data[0].data.remove(attach_card[0])
                    if self.data[0].data == []:
                        self.data.remove(self.data[0])
                        i -= 2
                        continue

            elif self.data[i].used_wildcard:
                if type(self.data[i].used_wildcard) == list:
                    if subtract_lists(self.data[i].used_wildcard, self.data[i].data):
                        self.data[i].data.extend(self.data[i].used_wildcard)    
                else:
                    if self.data[i].used_wildcard not in self.data[i].data:
                        self.data[i].data.append(self.data[i].used_wildcard)

            else:
                if i == 0:
                    if len(cards) == 14:
                        self.throw_card = get_highest_ranked_card(self.data[i].data)[0]
                        self.data[i].data.remove(self.throw_card)
                        if self.data[i].data == []:
                            self.data.remove(self.data[i])

            i -= 1

        if not self.throw_card:
            arranged_cards = []
            for i in range(len(self.data)-1,-1,-1):
                arranged_cards.extend(self.data[i].data)
            if len(cards) == 14:
                print(cards,"CARDS")
                print(arranged_cards,"ARRANGED CARDS")
                self.throw_card = deepcopy(subtract_lists(cards, arranged_cards))[0]
            else:
                self.throw_card = None

        total_sum = 0
        for i in range(len(self.data)-1,-1,-1):
            if self.data[i].reward == 0:
                pass
            else:
                total_sum += get_unformed_meld_sum(self.data[i].data)

        total_sum = -80 if total_sum <= -80 else total_sum

        self.reward_sum = total_sum
        num_cards_in_complete_melds = 0

        for node in self.data:
            if total_sum == 0:
                num_cards_in_complete_melds += len(node.data)
        
        if num_cards_in_complete_melds < 13 and num_cards_in_complete_melds != 0:
            remaining_wildcards = deepcopy(subtract_lists(my_wildcards, self.data[0].used_wildcards_until_now))
            self.data[0].data.extend(remaining_wildcards)    
        
        for node in self.data:
            print(node.data, end =",")
        print("Throw Card: ", self.throw_card, ", Post throw reward sum: ", total_sum, end =",")

        if total_sum == 0:
            print(" ******SHOW******")
        else:
            print(" NO SHOW")

'''
    identifies wildcards and joker from a player's list of cards
'''
def get_wildcards(cards):
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
    
'''
Gives depth/level of max_level leaf nodes
'''
def get_tree_depth():
    max_depth           = 0
    for node in all_nodes_list:
        if node.level > max_depth:
            max_depth   = node.level
    return max_depth

'''
Subtracts two card lists, even accepts lists with duplicate cards
'''
def subtract_lists(a, b):
    multiset_difference = Counter(a) - Counter(b)
    result              = []
    for i in a:
        if i in multiset_difference:
            result.append(i)
            multiset_difference -= Counter((i,))
    return result

'''
Checks if a given meld is a pure sequence or not
'''
def check_sequence_validity(cards):
    if cards in pure_sequences:
        return True
    else:
        return False

'''
Checks if a given meld is an impure sequence or not
'''
def check_impure_sequence_validity(cards):
    if cards in incomplete_sequences_houses:
        return True
    else:
        return False

'''
Checks if a given set is a complete set or not
'''
def check_complete_sets_validity(cards):
    if len(cards) == 3:
        if cards[0][:-1] == cards[1][:-1] and cards[0][:-1] == cards[2][:-1]:
            if  cards[0][-1] != cards[1][-1] and cards[0][-1] != cards[2][-1] and cards[1][-1] != cards[2][-1]:
                return True 
    if cards in complete_sets:
        return True
    else:
        return False

'''
Checks if a given meld is a house for set
'''
def check_sets_houses_validity(cards):
    if cards in incomplete_sets_houses:
        return True
    else:
        return False

'''
Checks if a given meld is a two cards break sequence
'''
def check_two_break_sequence_house_validity(cards):
    if cards in two_break_sequences_houses:
        return True
    else:
        return False

'''
Gives the sum of leaf node melds
'''
def get_unformed_meld_sum(cards):
    card_sum = 0
    for card in cards:
        if int(card[:-1]) <= 10:
            card_sum -= int(card[:-1])
        else:
            card_sum -= 10
    if card_sum <= -80:
        return -80
    else:
        return card_sum

'''
Identifies wildcards used until now to form melds
'''
def get_used_wildcard(node):
    if not node.data:
        remaining_wildcards = deepcopy(subtract_lists(my_wildcards,node.parent.used_wildcards_until_now))
        return [remaining_wildcards[0],remaining_wildcards[1]]
    
    if node.data in pure_sequences:
        for card in my_wildcards:
            if card in node.data:
                return card

    if node.data in incomplete_sequences_houses:
        remaining_wildcards = deepcopy(subtract_lists(my_wildcards,node.parent.used_wildcards_until_now))
        if remaining_wildcards and node.parent.reward_sum == 0 and node.level > 1:
            return remaining_wildcards[0]
    
    if node.data in incomplete_sets_houses and node.level > 2:
        remaining_wildcards = deepcopy(subtract_lists(my_wildcards,node.parent.used_wildcards_until_now))
        if remaining_wildcards and node.parent.reward_sum == 0 and node.level > 1:
            return remaining_wildcards[0]
    
    if (node.data in two_break_sequences_houses or len(node.data) == 1) and pure_sequences:
        remaining_wildcards = deepcopy(subtract_lists(my_wildcards,node.parent.used_wildcards_until_now))
        if len(remaining_wildcards) > 1 and node.level > 1: #for test
            return [remaining_wildcards[0],remaining_wildcards[1]]

'''
Builds root node
'''
def build_root():
    root                                        = TreeNode(cards)
    root.updated_cards_matrix                   = deepcopy(cards_matrix)
    root.updated_cards_matrix_without_wildcards = deepcopy(cards_matrix_without_wildcards)
    root.level                                  = root.get_level()
    root.cards_until_now                        = []
    root.melds_until_now                        = []
    root.reward                                 = 0
    root.reward_sum                             = 0
    print(root.level,":", root.data)
    all_nodes_list.append(root)

'''
Identifies wildcards not used until now to form melds
'''
def get_unused_wildcards(cards):
    unused_wildcards = []
    for card in cards:
        if card in my_wildcards:
            unused_wildcards.append(card)
    return unused_wildcards

'''
Identifies highest ranked card from a given meld/set of cards
'''
def get_highest_ranked_card(cards):
    highest_card = cards[0]
    for i in range(len(cards)):
        if int(highest_card[:-1]) < int(cards[i][:-1]):
            highest_card = cards[i]
    return [highest_card]

def populate_extra_cards():
    extra_cards_with_wildcard = deepcopy(cards)
    for node in all_nodes_list:
        if node.children:
            pass
        else:
            if pure_sequences and len(get_unused_wildcards(subtract_lists(extra_cards_with_wildcard, node.used_wildcards_until_now))) > 1:
                extra_cards = deepcopy(subtract_lists(extra_cards_with_wildcard, my_wildcards))
                extra_cards = deepcopy(subtract_lists(extra_cards, node.cards_until_now))
                if find_all_possible_two_break_sequence_houses(node.updated_cards_matrix):
                    test_card_matrix = fill_cards_matrix(extra_cards)
                    card = get_max_sum_meld(find_all_possible_two_break_sequence_houses(test_card_matrix))
                else:
                    if extra_cards:
                        card = get_highest_ranked_card(extra_cards)
                    else:
                        card = []
                if card:
                    child = TreeNode(card)
                    node.add_child(child)
                    child.get_updated_cards_matrix(child.data, node.updated_cards_matrix)
                    child.level = child.get_level()
                    child.cards_until_now = deepcopy(child.data)
                    child.cards_until_now.extend(child.parent.cards_until_now)
                    child.melds_until_now = deepcopy(child.parent.melds_until_now)
                    child.melds_until_now.extend([deepcopy(child.data)])
                    child.used_wildcard = get_used_wildcard(child)
                    child.used_wildcards_until_now = deepcopy(child.parent.used_wildcards_until_now)
                    child.used_wildcards_until_now.extend(child.used_wildcard)
                    child.reward = 0
                    child.reward_sum = child.parent.reward_sum
                    extra_cards_nodes.append(child)
                    extra_cards = deepcopy(subtract_lists(cards, child.cards_until_now))
                    extra_cards = deepcopy(subtract_lists(extra_cards, my_wildcards))
                    if extra_cards:
                        grand_child = TreeNode(extra_cards)
                        fill_child_data(grand_child, child)
                        extra_cards_nodes.append(grand_child)

            else:
                extra_cards = deepcopy(subtract_lists(extra_cards_with_wildcard, my_wildcards))
                extra_cards = deepcopy(subtract_lists(extra_cards, node.cards_until_now))
                if extra_cards:
                    child = TreeNode(extra_cards)
                    fill_child_data(child, node)
                    extra_cards_nodes.append(child)

    all_nodes_list.extend(extra_cards_nodes)

'''
Forms child node meld for a given meld node and populated the data
'''
def fill_child_data(child, node):
    node.add_child(child)
    child.get_updated_cards_matrix(child.data, node.updated_cards_matrix)
    child.level = child.get_level()
    child.cards_until_now = deepcopy(child.data)
    child.cards_until_now.extend(child.parent.cards_until_now)
    child.melds_until_now = deepcopy(child.parent.melds_until_now)
    child.melds_until_now.extend([deepcopy(child.data)])
    child.used_wildcard = get_used_wildcard(child)
    child.used_wildcards_until_now = deepcopy(child.parent.used_wildcards_until_now)
    if type(child.used_wildcard) == list:
        child.used_wildcards_until_now.extend(child.used_wildcard)
    else:
        child.used_wildcards_until_now.append(child.used_wildcard)
    if child.data == []:
        child.reward = 0
        child.reward_sum = child.parent.reward_sum
    else:
        eval_rewards(child)

'''
Compares if two melds are same
'''
def compare_melds(meld,nephews):
    meld = set([str(a) for a in meld])
    for nephew in nephews:
        if len(meld) == len(nephew.melds_until_now):
            if meld == set([str(a) for a in nephew.melds_until_now]):
                return True   
    return False 

'''
Method to build melds tree hierarchically
'''
def build_melds_tree():
    build_root()
    current_level = 0

    for _ in range(7):
        current_level_nodes = []
        for node in all_nodes_list:
            if node.level == current_level:
                current_level_nodes.append(node)

        for node in current_level_nodes:
            if find_all_possible_pure_sequences(node.updated_cards_matrix):
                if current_level == 0:
                    if find_all_possible_pure_sequences(node.updated_cards_matrix_without_wildcards):
                        node.get_updated_cards_matrix(my_wildcards,node.updated_cards_matrix) #Wildcards have been removed here *******
                    possible_pure_sequences = sort_meld_groups(find_all_possible_pure_sequences(node.updated_cards_matrix))
                    for sequence in possible_pure_sequences:
                        # if [sequence,node.data] not in node.get_sibling_nephew_pair():
                        if not compare_melds(node.melds_until_now+[sequence],node.get_nephews()):
                            child = TreeNode(sequence)
                            fill_child_data(child, node)
                            all_nodes_list.append(child)
                
                if current_level > 0 and find_all_possible_pure_sequences(node.updated_cards_matrix):
                    sequences_list = find_all_possible_pure_sequences(node.updated_cards_matrix)
                    incomplete_sequences_list = find_all_possible_incomplete_sequences(node.updated_cards_matrix)
                    combined_list = sort_meld_groups(sequences_list + incomplete_sequences_list)
                    for meld in combined_list:
                        # if [meld,node.data] not in node.get_sibling_nephew_pair():
                        if not compare_melds(node.melds_until_now+[meld],node.get_nephews()):
                            child = TreeNode(meld)
                            fill_child_data(child, node)
                            all_nodes_list.append(child)
                            
            else:
                node.get_updated_cards_matrix(my_wildcards,node.updated_cards_matrix) #Wildcards have been removed here *******

                if node.level <= 1:
                    if find_all_possible_incomplete_sequences(node.updated_cards_matrix):
                        possible_incomplete_sequences = sort_meld_groups(find_all_possible_incomplete_sequences(node.updated_cards_matrix))
                        if node.level == 1 and pure_sequences and len(get_unused_wildcards(subtract_lists(cards, node.used_wildcards_until_now))) > 1:
                            possible_incomplete_sequences.append([])
                        for sequence_house in possible_incomplete_sequences:
                            # if [sequence_house,node.data] not in node.get_sibling_nephew_pair():
                            if not compare_melds(node.melds_until_now+[sequence_house],node.get_nephews()):
                                child = TreeNode(sequence_house)
                                fill_child_data(child, node)
                                all_nodes_list.append(child)
                    
                    if node.level == 1 and pure_sequences and not find_all_possible_incomplete_sequences(node.updated_cards_matrix) \
                        and len(get_unused_wildcards(subtract_lists(cards, node.used_wildcards_until_now))) > 1:

                        if find_all_possible_two_break_sequence_houses(node.updated_cards_matrix):
                            houses = find_all_possible_two_break_sequence_houses(node.updated_cards_matrix)
                            houses.append([])
                        else:
                            houses = [[]]
                        
                        for house in houses:
                            child = TreeNode(house)
                            fill_child_data(child, node)
                            all_nodes_list.append(child)
                
                seq_house_not_found = (node.level <= 1 and not find_all_possible_incomplete_sequences(node.updated_cards_matrix)) or \
                                        not (node.level == 1 and find_all_possible_two_break_sequence_houses(node.updated_cards_matrix) and \
                                            len(get_unused_wildcards(subtract_lists(cards, node.used_wildcards_until_now))) > 1)
                
                if seq_house_not_found or node.level > 1:
                    if find_all_possible_complete_sets(node.updated_cards_matrix):
                        possible_complete_sets = sort_meld_groups(find_all_possible_complete_sets(node.updated_cards_matrix))
                        for complete_set in possible_complete_sets:
                            # if [complete_set,node.data] not in node.get_sibling_nephew_pair():
                            if not compare_melds(node.melds_until_now+[complete_set],node.get_nephews()):
                                child = TreeNode(complete_set)
                                fill_child_data(child, node)
                                all_nodes_list.append(child)
                    
                    else:
                        sequence_houses = find_all_possible_incomplete_sequences(node.updated_cards_matrix)
                        sets_houses = find_all_possible_sets_houses(node.updated_cards_matrix)
                        incomplete_melds = sort_meld_groups(sets_houses + sequence_houses)
                        if incomplete_melds:
                            for meld in incomplete_melds:
                                # if [meld,node.data] not in node.get_sibling_nephew_pair():
                                if not compare_melds(node.melds_until_now+[meld],node.get_nephews()):
                                    child = TreeNode(meld)
                                    fill_child_data(child, node)
                                    all_nodes_list.append(child)

        current_level += 1
    populate_extra_cards()
    # all_nodes_list[0].print_tree()

'''
Evaluates sum of cards for each meld, and cumulative sum until that node hierarchically
'''
def eval_rewards(node):
    remaining_wildcards = deepcopy(subtract_lists(my_wildcards, node.parent.used_wildcards_until_now))

    if node.level == 0:
        node.reward = 0
        node.reward_sum = 0
    
    elif node.level == 1:
        if check_sequence_validity(node.data):
            node.reward = 0
        else:
            node.reward = get_unformed_meld_sum(node.data)
        node.reward_sum = node.reward
    
    elif node.level == 2:
        if check_sequence_validity(node.data):
            node.reward = 0
        elif check_impure_sequence_validity(node.data) and node.parent.reward_sum == 0 and remaining_wildcards:
            # print("SATISFIED: ",remaining_wildcards, "CARDS: ", node.data)
            node.reward = 0
        # elif check_two_break_sequence_house_validity(node.data) and node.parent.reward_sum == 0 and remaining_wildcards:  #check test
        elif check_two_break_sequence_house_validity(node.data) and pure_sequences and remaining_wildcards:
            node.reward = 0
        else:
            # print("NOT SATISFIED: ",remaining_wildcards, "CARDS: ", node.data)
            node.reward = get_unformed_meld_sum(node.data)
        node.reward_sum = node.reward + node.parent.reward_sum if (node.reward + node.parent.reward_sum) >= -80 else -80 
    
    else:
        if check_sequence_validity(node.data):
            node.reward = 0
        elif check_impure_sequence_validity(node.data) and node.parent.reward_sum == 0 and remaining_wildcards:
            node.reward = 0
        elif check_impure_sequence_validity(node.data) and node.parent.reward_sum != 0:
            node.reward = get_unformed_meld_sum(node.data)
        elif check_complete_sets_validity(node.data) and node.parent.reward_sum == 0:
            node.reward = 0
        elif check_complete_sets_validity(node.data) and node.parent.reward == 0 and pure_sequences:
            node.reward = 0
        elif check_complete_sets_validity(node.data) and node.parent.reward_sum != 0:
            node.reward = get_unformed_meld_sum(node.data)
        elif check_sets_houses_validity(node.data) and node.parent.reward_sum == 0 and remaining_wildcards:
            node.reward = 0
        elif check_sets_houses_validity(node.data) and node.parent.reward_sum != 0:
            node.reward = get_unformed_meld_sum(node.data)
        else:
            node.reward = get_unformed_meld_sum(node.data)

        node.reward_sum = node.reward + node.parent.reward_sum if (node.reward + node.parent.reward_sum) >= -80 else -80

    # if you dont have sequences then add the values of non joker wildcards also
    # if not node.children:
    #     if pure_sequences:
    #         pass
    #     else:
    #         for card in my_wildcards:
    #             if int(card[:-1]) == 15:
    #                 pass
    #             else:
    #                 if int(card[:-1]) > 10:
    #                     node.reward_sum += 10
    #                 else:
    #                     node.reward_sum += int(card[:-1])
    #                 node.reward_sum = -80 if node.reward_sum < -80 else node.reward_sum

'''
Evaluates sum of cards for a given meld
'''
def meld_sum(meld):
    sum = 0
    for item in meld:
        if int(item[:-1]) > 10:
            sum += 10
        else:
            sum += int(item[:-1])
    return sum

'''
Evaluates the meld which has maximum sum of its cards
'''
def get_max_sum_meld(melds):
    if len(melds) == 0:
        return
    if len(melds) == 1:
        return melds[0]
    else:
        max_sum_meld = meld_sum(melds[0])
        for meld in melds:
            if type(max_sum_meld) == int:
                if meld_sum(meld) > max_sum_meld:
                    max_sum_meld = meld
            else:
                if meld_sum(meld) > meld_sum(max_sum_meld):
                    max_sum_meld = meld
        return  max_sum_meld
            
'''
Sorts melds of cards
'''
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

'''
Evaluates best combination of meld groups or the one having lowest card sum
'''
def find_best_combinations():
    max_reward_sum = -80
    for node in all_nodes_list:
        if not node.children:
            if node.reward_sum >= max_reward_sum:
                max_reward_sum = node.reward_sum
    
    max_reward_nodes_list = []
    for node in all_nodes_list:
        if not node.children:
            if node.reward_sum >= max_reward_sum - 10: #only to check
                max_reward_nodes_list.append(node)
    
    return max_reward_nodes_list

def print_best_melds(max_rewards_nodes_list):
    best_melds = []
    for node in max_rewards_nodes_list:
        melds = []
        dummy_node = node
        p = dummy_node.parent
        while p:
            melds.append(dummy_node)
            dummy_node = p
            p = p.parent
        test_card_matrix = fill_cards_matrix(melds[0].data)
        if  (find_all_possible_incomplete_sequences(test_card_matrix) or \
            find_all_possible_pure_sequences(test_card_matrix) or \
            find_all_possible_complete_sets(test_card_matrix)or \
            find_all_possible_sets_houses(test_card_matrix)) and len(cards) == 14:
            continue
        else:
            best_melds.append(melds)
        for each in melds:
            if each.used_wildcard:
                if check_sequence_validity(each.data):
                    print(each.data, end = ",")
                else:
                    wc = []
                    if type(each.used_wildcard) == list:
                        wc = deepcopy(each.used_wildcard)
                    else:
                        wc.append(each.used_wildcard)
                    print(each.data + wc, end = ",")
            else:
                print(each.data, end = ",")
        print("Reward Sum: ",node.reward_sum)
    
    return best_melds

'''
Evaluates the best card to throw from the options of leaf node cards
'''
def find_card_to_throw(best_melds):
    extra_cards_nodes = []
    lowest_extra_cards_meld_length = 14
    smallest_extra_cards_melds = []
    throwable_cards = []

    for melds in best_melds:
        extra_cards_nodes.append(melds[0])
        if len(melds[0]) < lowest_extra_cards_meld_length and len(melds[0]) > 0:
            lowest_extra_cards_meld_length = len(melds[0])

    for meld in extra_cards_nodes:
        if len(meld) == lowest_extra_cards_meld_length:
            if meld not in smallest_extra_cards_melds:
                smallest_extra_cards_melds.append(meld)
    
    print(smallest_extra_cards_melds)
    
    for card in smallest_extra_cards_melds[0]:
        throwable_cards.append(card)
        for other_meld in smallest_extra_cards_melds:
            if other_meld != smallest_extra_cards_melds[0]:
                if card not in other_meld:
                    if card in throwable_cards:
                        throwable_cards.remove(card)
    
    if not throwable_cards:
        throwable_cards = list(np.concatenate(smallest_extra_cards_melds).flat)

    print("THROWABLE CARDS: ",throwable_cards)
    highest_card = throwable_cards[0]
    for i in range(len(throwable_cards)):
        if int(highest_card[:-1]) < int(throwable_cards[i][:-1]):
            highest_card = throwable_cards[i]

    return highest_card

'''
Evaluates the best card to throw from the options of leaf node cards(modified method from upper one)
'''
def find_card_to_throw_new(best_melds_obj_list):
    extra_cards_nodes = []
    lowest_extra_cards_meld_length = 14
    smallest_extra_cards_melds = []
    throwable_cards = []

    for melds in best_melds_obj_list:
        extra_cards_nodes.append(melds.data[0].data)
        if len(melds.data[0].data) < lowest_extra_cards_meld_length and len(melds.data[0].data) > 0:
            lowest_extra_cards_meld_length = len(melds.data[0].data)

    for meld in extra_cards_nodes:
        if len(meld) == lowest_extra_cards_meld_length:
            if meld not in smallest_extra_cards_melds:
                smallest_extra_cards_melds.append(meld)
    
    print(smallest_extra_cards_melds)
    
    for card in smallest_extra_cards_melds[0]:
        throwable_cards.append(card)
        for other_meld in smallest_extra_cards_melds:
            if other_meld != smallest_extra_cards_melds[0]:
                if card not in other_meld:
                    if card in throwable_cards:
                        throwable_cards.remove(card)
    
    if not throwable_cards:
        throwable_cards = list(np.concatenate(smallest_extra_cards_melds).flat)

    print("THROWABLE CARDS: ",throwable_cards)
    highest_card = throwable_cards[0]
    for i in range(len(throwable_cards)):
        if int(highest_card[:-1]) < int(throwable_cards[i][:-1]):
            highest_card = throwable_cards[i]

    return highest_card


all_nodes_list = []
extra_cards_nodes = []
my_wildcards = []
tree_depth = get_tree_depth()
maximum_sum_meld = -80


if __name__ == '__main__':
    start = time()
    get_wildcards(cards)
    print("MY WILDCARDS: ",my_wildcards)
    build_melds_tree()
    best_melds_obj_list = []
    max_rewards_nodes_list = find_best_combinations()
    best_melds = deepcopy(print_best_melds(max_rewards_nodes_list))
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    total_time = 0
    for melds in best_melds:
        start_1 = time()
        best_melds_obj_list.append(Melds(melds))
        end_1 = time()
        total_time += (end_1- start_1)
        # print(total_time)

    print("MAX TREE DEPTH IS:", get_tree_depth())
    print("TOTAL NODES: ", len(all_nodes_list))
    end = time()
    print("TOTAL TIME: ", end - start)

