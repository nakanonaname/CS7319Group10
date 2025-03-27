class WinChecker:
    def __init__(self, blackboard):
        self.blackboard = blackboard

    def check_winner(self):
        board = self.blackboard.board
        for row in range(6):
            for col in range(7):
                player = board[row][col]
                if player == 0:
                    continue 
                # check the horizontal win
                if col + 3 < 7 and all(board[row][col + i] == player for i in range(4)):
                    return player, [(row, col + i) for i in range(4)]
                # check the vertical win
                if row + 3 < 6 and all(board[row + i][col] == player for i in range(4)):
                    return player, [(row + i, col) for i in range(4)]
                # check the diagonal (down-right) win
                if row + 3 < 6 and col + 3 < 7 and all(board[row + i][col + i] == player for i in range(4)):
                    return player, [(row + i, col + i) for i in range(4)]
                # check the diagonal (up-right) win
                if row - 3 >= 0 and col + 3 < 7 and all(board[row - i][col + i] == player for i in range(4)):
                    return player, [(row - i, col + i) for i in range(4)]

        # check if there is no empty slots left, the game is  draw
        if all(board[0][col] != 0 for col in range(7)):  
            return 0, None  

        return None, None  
