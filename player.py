class Player:
    def __init__(self,position):
        self.position = position
        self.cards = []
        self.sorted_cards = []

# positions = ["B","R","T","L"]
positions = ["Me","Opp"]
players = []
for position in positions:
    player = Player(position)
    players.append(player)
