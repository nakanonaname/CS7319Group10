import tkinter as tk
from MoveProcessor import MoveProcessor
from MoveValidator import MoveValidator
from PlayerManager import PlayerManager
from WinCheck import WinChecker
from MonteCarlo import MonteCarlo

class GameBoard(tk.Canvas):
    def __init__(self, parent, blackboard, start_new_game_callback, restart_game_callback, app_ref):
        super().__init__(parent)
        self.blackboard = blackboard
        self.start_new_game_callback = start_new_game_callback
        self.restart_game_callback = restart_game_callback
        self.app_ref = app_ref

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg='blue', height=360, width=420)
        self.canvas.pack(side=tk.LEFT, padx=(10, 0))
        self.draw_board()

        self.canvas.bind("<Button-1>", self.on_board_click)

    def draw_board(self, winning_positions=None):
        self.canvas.delete("token")
        cell_size = 60  

        for row in range(6):
            for col in range(7):
                x0, y0 = col * cell_size, row * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                color = "white"

                if self.blackboard.board[row][col] == 1:
                    color = "yellow"
                elif self.blackboard.board[row][col] == 2:
                    color = "red"

                self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill=color, tags="token")

    def on_board_click(self, event):
        column = event.x // 60
        MV = MoveValidator(self.blackboard)
        MP = MoveProcessor(self.blackboard, MV)
        PM = PlayerManager(self.blackboard)
        Win = WinChecker(self.blackboard)

        if MP.process_move(column):  
            self.draw_board()  
            
            winner, winning_positions = Win.check_winner()
            if winner:
                self.draw_board(winning_positions)
                self.after(2000, lambda: self.app_ref.show_winner(winner))
                return

            PM.switch_turns()
            
            if self.blackboard.opponent_type == "Monte Carlo AI" and self.blackboard.current_player == 2:
                self.after(500, self.ai_make_move)  

    def ai_make_move(self):
        if self.blackboard.opponent_type == "Monte Carlo AI":
            MC = MonteCarlo(self.blackboard)
            move = MC.find_best_move()
            if move is not None:
                self.on_board_click(type('', (), {'x': move * 60})()) 
