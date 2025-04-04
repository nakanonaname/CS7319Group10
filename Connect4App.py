import tkinter as tk
from StartMenu import StartMenu
from GameBoard import GameBoard
from WinnerDisplay import WinnerDisplay
from Blackboard import Blackboard
from ColorSelector import ColorSelector

class Connect4App:
    def __init__(self, root, blackboard):
        self.root = root
        self.start_menu = StartMenu(
            root,
            start_game_callback=self.start_game,
            open_color_selector_callback=self.open_color_selector
        )
        self.start_menu.pack()
        self.blackboard = blackboard
        self.game_board = None
        self.winner_display = None  # Initialize to avoid errors

    def start_game(self, opponent):
        # Hide the winner display if it exists
        if hasattr(self, 'winner_display') and self.winner_display:
            self.winner_display.pack_forget()
        # Hide the game board if it exists
        if self.game_board:
            self.game_board.pack_forget()
        #create a new game board based on the selected opponent
        self.blackboard.opponent_type = opponent 
        self.game_board = GameBoard(self.root, self.blackboard, self.start_new_game, self.restart_game, self)
        self.game_board.pack()
        # Hide the start menu ui 
        self.start_menu.pack_forget()

    def open_color_selector(self, opponent):
        self.start_menu.pack_forget()
        self.color_selector = ColorSelector(
            self.root,
            on_done_callback=lambda colors: self.receive_colors_and_start_game(opponent, colors)
        )
        self.color_selector.pack()

    def receive_colors_and_start_game(self, opponent, colors):
        self.blackboard.selected_colors = colors  # 保存用户选择的颜色
        self.color_selector.pack_forget()
        self.start_game(opponent)

    def start_new_game(self):
        """Resets the game and brings back the start menu."""
        # Hide the winner display if it exists
        if self.winner_display:
            self.winner_display.pack_forget()
        self.blackboard.board = [[0 for _ in range(7)] for _ in range(6)]
        self.blackboard.current_player = 1  
        if self.game_board:
            self.game_board.pack_forget()
        self.start_menu.pack()

    def restart_game(self):
        """Resets the board without returning to the main menu."""
        self.blackboard.board = [[0 for _ in range(7)] for _ in range(6)]
        self.blackboard.current_player = 1  
        if self.game_board:
            self.game_board.draw_board()
            self.game_board.update_player_turn_label()

    def show_winner(self, winner):
        """Redirect the user to a new ui to indiacte the result of the game."""
        if self.game_board:
            self.game_board.pack_forget()  
        self.winner_display = WinnerDisplay(self.root, winner, self.start_new_game, self.replay_game)
        self.winner_display.pack()

    def replay_game(self):
        """Replays the last game with the same settings."""
        self.blackboard.board = [[0 for _ in range(7)] for _ in range(6)]
        self.blackboard.current_player = 1  
        self.start_game(self.blackboard.opponent_type)
        if self.winner_display:
            self.winner_display.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect 4")
    app = Connect4App(root, Blackboard())
    root.mainloop()
