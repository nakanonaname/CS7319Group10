import tkinter as tk
import numpy as np
from game_session_layer import GameSessionLayer, GameMode, PLAYER_1


class UILayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.root.geometry("700x800")
        self.root.configure(bg="white")
        self.display_menu_page()
        self.cell_size = 80

        self._game_session_layer = GameSessionLayer()
        self.canvas = None
        self.cells = None
        self.final_result = None

    def display_menu_page(self):
        self.clear_window()

        label = tk.Label(self.root,
                         text="Connect 4",
                         font=("Arial", 28),
                         fg="black",
                         bg="white")

        label.pack(pady=30)

        btn_two_players = tk.Button(self.root,
                                    text="Multiplayer",
                                    font=("Arial", 18),
                                    bg="white",
                                    fg="black",
                                    width=15,
                                    height=2,
                                    command=self.display_multiplayer_game_ui)
        btn_two_players.pack(pady=15)

        btn_ai = tk.Button(self.root,
                           text="AI Player",
                           font=("Arial", 18),
                           bg="white",
                           fg="black",
                           width=15,
                           height=2,
                           command=self.display_single_player_game_ui)
        btn_ai.pack(pady=15)

        btn_exit = tk.Button(self.root,
                             text="Exit",
                             font=("Arial", 18),
                             bg="white",
                             fg="black",
                             width=15,
                             height=2,
                             command=self.root.quit)
        btn_exit.pack(pady=30)

    def display_multiplayer_game_ui(self):
        self.show_game_ui(game_mode=GameMode.MULTI_PLAYER)

    def display_single_player_game_ui(self):
        self.show_game_ui(game_mode=GameMode.SINGLE_PLAYER)

    def show_game_ui(self, game_mode: GameMode):
        self.clear_window()
        board = self._game_session_layer.start_game(game_mode)
        self.cells = np.zeros((board.width, board.height), dtype=int)

        menu_frame = tk.Frame(self.root, bg="white")
        menu_frame.pack(pady=10)

        btn_restart = tk.Button(menu_frame,
                                text="Restart",
                                font=("Arial", 16),
                                bg="white",
                                fg="black",
                                width=12,
                                height=1,
                                command=self.restart)
        btn_restart.pack(side="left", padx=40)

        btn_exit = tk.Button(menu_frame,
                             text="Exit",
                             font=("Arial", 16),
                             bg="white",
                             fg="black",
                             width=12,
                             height=1,
                             command=self.root.quit)
        btn_exit.pack(side="left", padx=40)

        btn_end = tk.Button(self.root,
                            text="End Game",
                            font=("Arial", 18),
                            bg="white",
                            fg="black",
                            width=15,
                            height=2,
                            command=self.display_end_page)
        btn_end.pack(pady=30)

        label = tk.Label(self.root,
                         text=f"{game_mode} - In Game",
                         font=("Arial", 22),
                         fg="black",
                         bg="white")
        label.pack(pady=20)

        self.canvas = tk.Canvas(self.root,
                                width=700,
                                height=600,
                                bg="white",
                                highlightthickness=0)
        self.canvas.bind("<Button-1>", self.handle_cell_click)
        self.canvas.pack()

        self.display_board()

    def restart(self):
        self.show_game_ui(self._game_session_layer.game_mode)

    def display_board(self):
        for x in range(len(self.cells[0])):
            for y in range(len(self.cells)):
                x1, y1 = y * self.cell_size + 10, x * self.cell_size + 10
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                self.cells[y, x] = self.canvas.create_oval(x1, y1, x2, y2, fill="gray", outline="white")

    def handle_cell_click(self, event):
        # Convert click coordinates to grid position
        x = event.x // self.cell_size

        if 0 <= x <= len(self.cells[0]):
            move_result = self._game_session_layer.move(x)
            for (x, y, player) in move_result.moves:
                fill = "red" if player == PLAYER_1 else "yellow"
                self.canvas.itemconfig(self.cells[x, y], fill=fill)

            if move_result.is_over:
                self.final_result = move_result
                self.display_end_page()

    def display_end_page(self):
        self.clear_window()
        board = self._game_session_layer.end_game()
        self.cells = np.zeros((board.width, board.height), dtype=int)

        label = tk.Label(self.root,
                         text="Game Over",
                         font=("Arial", 28),
                         fg="black",
                         bg="white")
        label.pack(pady=30)

        text = "Game ended"
        if self.final_result is not None:
            if self.final_result.is_draw:
                text = "Draw!"
            elif self.final_result.game_mode == GameMode.MULTI_PLAYER:
                text = "Player 1 Wins!" if self.final_result.winner == PLAYER_1 else "Player 2 Wins!"
            else:
                text = "You Win!" if self.final_result.winner == PLAYER_1 else "You Lose!"

        winner_label = tk.Label(self.root,
                                text=text,
                                font=("Arial", 22),
                                fg="black",
                                bg="white")
        winner_label.pack(pady=10)

        btn_restart = tk.Button(self.root,
                                text="Back",
                                font=("Arial", 18),
                                bg="white",
                                fg="black",
                                width=15,
                                height=2,
                                command=self.display_menu_page)
        btn_restart.pack(pady=15)

        btn_exit = tk.Button(self.root,
                             text="Exit",
                             font=("Arial", 18),
                             bg="white",
                             fg="black",
                             width=15,
                             height=2,
                             command=self.root.quit)
        btn_exit.pack(pady=15)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def draw(self):
        self.root.mainloop()


if __name__ == "__main__":
    UILayer().draw()
