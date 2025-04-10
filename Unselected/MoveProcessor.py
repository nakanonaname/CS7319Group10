class MoveProcessor:
    def __init__(self, blackboard, move_validator):
        self.blackboard = blackboard
        self.move_validator = move_validator

    def process_move(self, column):
        # check if the move valid
        if not self.move_validator.is_move_valid(column):
            return False

        # place the token if the slot is empty
        for row in reversed(range(6)): 
            if self.blackboard.board[row][column] == 0:  
                self.blackboard.board[row][column] = self.blackboard.current_player  
                return True

        return False
