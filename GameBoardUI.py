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
        self.colors = self.blackboard.selected_colors if hasattr(self.blackboard, "selected_colors") else {}

        self.create_widgets()

    def create_widgets(self):
        bg_color = self.colors.get("background_color", "blue")
        self.canvas = tk.Canvas(self, bg=bg_color, height=360, width=420)

        self.canvas.pack(side=tk.LEFT, padx=(10, 0))
        self.draw_board()

        self.right_side_frame = tk.Frame(self)
        self.right_side_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 10))

        self.new_game_button = tk.Button(self.right_side_frame, text="Start New Game", command=self.start_new)
        self.new_game_button.pack(pady=10)

        self.restart_button = tk.Button(self.right_side_frame, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(pady=10)

        self.player_turn_label = tk.Label(self, text="player 1's turn")
        self.player_turn_label.pack(side=tk.BOTTOM, pady=(10, 10))

        self.canvas.bind("<Button-1>", self.on_board_click)

    def update_player_turn_label(self):
        player_color = "player 1" if self.blackboard.current_player == 1 else "player 2"
        self.player_turn_label.config(text=f"{player_color}'s turn")

    def draw_board(self, winning_positions=None):
        self.canvas.delete("token")
        self.update_idletasks() 

        rows, cols = 6, 7
        cell_size = 60  

        for row in range(rows):
            for col in range(cols):
                x0, y0 = col * cell_size, row * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                color = "white"

                if self.blackboard.board[row][col] == 1:
                    color = self.colors.get("player1_color", "player 1")
                elif self.blackboard.board[row][col] == 2:
                    color = self.colors.get("player2_color", "player 2")
                else:
                    color = self.colors.get("board_color", "white")

                self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill=color, tags="token")

        if winning_positions:
            x0, y0 = winning_positions[0][1] * cell_size + 30, winning_positions[0][0] * cell_size + 30
            x1, y1 = winning_positions[-1][1] * cell_size + 30, winning_positions[-1][0] * cell_size + 30
            self.canvas.create_line(x0, y0, x1, y1, fill="black", width=5)
        #  make sure that the board is refreshed
        self.update_idletasks()  

    def on_board_click(self, event):
        if hasattr(self, "waiting_for_winner") and self.waiting_for_winner:
            # output for debugging
            print("Click ignored: Waiting for winner screen to appear...")
            return
        
        column = event.x // 60

        MV = MoveValidator(self.blackboard)
        MP = MoveProcessor(self.blackboard, MV)
        PM = PlayerManager(self.blackboard)
        Win = WinChecker(self.blackboard)

        if MP.process_move(column):  
            self.draw_board()  

            winner, winning_positions = Win.check_winner()
            if winner is not None:  
                # prevent the user from clicking(choosing a column) if there is a winner and the line drawn but the win ui not redirected yet
                self.waiting_for_winner = True  
                self.draw_board(winning_positions if winning_positions else None)
                # show winner and unlock clicks
                self.after(2000, lambda: self.show_winner_and_unlock(winner))  
                return

            PM.switch_turns()
            self.update_player_turn_label()

            if self.blackboard.opponent_type == "Monte Carlo AI" and self.blackboard.current_player == 2:
                self.after(500, self.ai_make_move)

    def show_winner_and_unlock(self, winner):
        self.app_ref.show_winner(winner) 
        self.waiting_for_winner = False 

    def ai_make_move(self):
        if self.blackboard.opponent_type == "Monte Carlo AI":
            MC = MonteCarlo(self.blackboard)
            move = MC.find_best_move()

            if move is None:
                return  

            MV = MoveValidator(self.blackboard)
            MP = MoveProcessor(self.blackboard, MV)
            PM = PlayerManager(self.blackboard)
            Win = WinChecker(self.blackboard)

            if MP.process_move(move):  
                self.draw_board()  

                winner, winning_positions = Win.check_winner()
                if winner:
                    self.draw_board(winning_positions)
                    self.after(2000, lambda: self.app_ref.show_winner(winner))
                    return

                PM.switch_turns()
                self.update_player_turn_label()

    def restart_game(self):
        self.restart_game_callback()

    def start_new(self):
        self.start_new_game_callback()

