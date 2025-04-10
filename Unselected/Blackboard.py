class Blackboard:
    def __init__(self):
        # Initialize the board with a 6x7 grid filled with 0s.
        # 0 represents empty(no tokens), 1 and 2 represent player 1 and 2's tokens.
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.opponent_type = 'Monte Carlo AI'
