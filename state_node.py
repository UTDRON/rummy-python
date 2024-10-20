from collections import defaultdict

class StateNode:
    def __init__(self,player):
        # self.legal_cards = player.legal_cards
        self.state = player.legal_cards
        self.children = set()
        self.parent = None
        self.N = 0 #Number of times parent node has been visited(used in UCB)
        self.n = 0 #Number of times current node has been visited(used in UCB)
        self.v = 0 #Exploitation factor of current node(used in UCB)
        #UCB means Upper Confidence Bound which is a factor that decides which node evaluate next in order to maximize
        # probability of victory from the given state. It generally consists of two factors, Exploitation and Exploration.

class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def get_legal_actions(self):
        # return legal_cards
        pass

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses #returns the difference of wins - losses

    def n(self):
        return self._number_of_visits #returns the number of times each node is visited.

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node #all the possible child nodes corresponding to generated states are appended to the children array and the child_node is returned

    def is_terminal_node(self):
        return self.state.is_game_over()  #check if the current node is terminal or not. Terminal node is reached when the game is over.

    def rollout(self):
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():

            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()