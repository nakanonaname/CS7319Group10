class MoveValidator:
    def __init__(self, blackboard):
        self.blackboard = blackboard

    def is_move_valid(self, column):
        # check if the choosen column is valid 
        if column < 0 or column >= len(self.blackboard.board[0]):
            return False

        for row in range(len(self.blackboard.board) - 1, -1, -1):  
            if self.blackboard.board[row][column] == 0:
                return True 

        return False  


