import tkinter as tk
import numpy as np
from game_session_layer import GameSessionLayer, GameMode, PLAYER_1, MoveResult


class UILayer(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4 - Layered")
        self.root.geometry("500x500")
        self.display_menu_page()
        self.cell_size = 50
        self.cell_padding = 10

        self._game_session_layer = GameSessionLayer()
        self.player_turn_label = None
        self.canvas = None
        self.cells = None

    def display_menu_page(self):
        self.clear_window()

        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=20)

        title_connect = tk.Label(title_frame,
                                 text="Connect",
                                 fg="red",
                                 font=("Helvetica", 24, "bold"))
        title_connect.pack(side=tk.LEFT)

        title_four = tk.Label(title_frame,
                              text="-4",
                              fg="yellow",
                              font=("Helvetica", 24, "bold"))
        title_four.pack(side=tk.LEFT)

        label = tk.Label(self.root,
                         text="Choose your opponent:",
                         font=("Helvetica", 14))
        label.pack(pady=20)

        radio_frame = tk.Frame(self.root)
        radio_frame.pack(pady=10)

        self.game_mode_var = tk.StringVar(value="SINGLEPLAYER")
        ai_radio_btn = tk.Radiobutton(radio_frame,
                                      text="Monte Carlo AI",
                                      variable=self.game_mode_var,
                                      value="SINGLE_PLAYER",
                                      font=("Helvetica", 12))
        ai_radio_btn.pack(anchor=tk.W, pady=5)
        multi_player_btn = tk.Radiobutton(radio_frame,
                                          text="2 Players",
                                          variable=self.game_mode_var,
                                          value="MULTIPLAYER",
                                          font=("Helvetica", 12))
        multi_player_btn.pack(anchor=tk.W, pady=5)

        start_button = tk.Button(self.root,
                                 text="Start Game",
                                 font=("Helvetica", 14),
                                 command=self.start_game)
        start_button.pack(pady=20)

    def start_game(self):
        game_mode = GameMode.SINGLE_PLAYER if self.game_mode_var.get() == "SINGLE_PLAYER" else GameMode.MULTI_PLAYER
        self.show_game_ui(game_mode=game_mode)

    def show_game_ui(self, game_mode: GameMode):
        self.clear_window()

        self.root.geometry("670x400")
        self.root.minsize(670, 400)
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        main_container.grid_columnconfigure(0, weight=3, minsize=400)
        main_container.grid_columnconfigure(1, weight=1, minsize=200)
        main_container.grid_rowconfigure(0, weight=1)

        board = self._game_session_layer.start_game(game_mode)
        self.cells = np.zeros((board.width, board.height), dtype=int)

        game_frame = tk.Frame(main_container, width=400, height=200)
        game_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        game_frame.grid_propagate(False)

        self.canvas = tk.Canvas(game_frame,
                                width=400,
                                height=400,
                                bg="blue")
        self.canvas.bind("<Button-1>", self.handle_cell_click)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        menu_frame = tk.Frame(main_container, width=200)
        menu_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        btn_start_game = tk.Button(menu_frame,
                                   text="Start New Game",
                                   font=("Arial", 16),
                                   bg="white",
                                   width=12,
                                   height=1,
                                   command=self.display_menu_page)
        btn_start_game.pack(pady=10)

        btn_restart = tk.Button(menu_frame,
                                text="Restart Game",
                                font=("Arial", 16),
                                bg="white",
                                width=12,
                                height=1,
                                command=self.restart)
        btn_restart.pack(pady=10)

        spacer = tk.Frame(menu_frame)
        spacer.pack(fill=tk.BOTH, expand=True)

        if self._game_session_layer.is_multiplayer:
            self.player_turn_label = tk.Label(
                menu_frame,
                text="Player Turn: Player 1",
                font=("Arial", 10),
                justify=tk.LEFT
            )
            self.player_turn_label.pack(side=tk.BOTTOM, pady=15)

        player_legend_yellow_text = tk.Label(
            menu_frame,
            text="Player 2" if self._game_session_layer.is_multiplayer else "Monte Carlo AI",
            font=("Arial", 10),
            fg="yellow",
            justify=tk.LEFT
        )
        player_legend_yellow_text.pack(side=tk.BOTTOM)

        player_legend_red_text = tk.Label(
            menu_frame,
            text="Player 1",
            font=("Arial", 10),
            highlightcolor="red",
            fg="red",
            justify=tk.LEFT
        )
        player_legend_red_text.pack(side=tk.BOTTOM)

        self.display_board()

    def restart(self):
        self.show_game_ui(self._game_session_layer.game_mode)

    def update_player_turn_label(self):
        current = "Player 1" if self._game_session_layer.current_player == PLAYER_1 else "Player 2"
        self.player_turn_label.config(text=f"Player Turn: {current}")

    def display_board(self):
        for x in range(len(self.cells[0])):
            for y in range(len(self.cells)):
                x1 = y * (self.cell_size + self.cell_padding) + 10
                y1 = x * (self.cell_size + self.cell_padding) + 10
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.cells[y, x] = self.canvas.create_oval(x1, y1, x2, y2, fill="white")

    def handle_cell_click(self, event):
        # Convert click coordinates to grid position
        x = event.x // (self.cell_size + self.cell_padding)

        if 0 <= x <= len(self.cells[0]):
            move_result = self._game_session_layer.move(x)
            for (x, y, player) in move_result.moves:
                fill = "red" if player == PLAYER_1 else "yellow"
                self.canvas.itemconfig(self.cells[x, y], fill=fill)

            if self._game_session_layer.is_multiplayer:
                self.update_player_turn_label()

            if move_result.is_over:
                self.display_end_page(move_result)

    def display_end_page(self, result: MoveResult):
        self.clear_window()
        board = self._game_session_layer.end_game()
        self.cells = np.zeros((board.width, board.height), dtype=int)

        label = tk.Label(self.root,
                         text="Game Over",
                         font=("Arial", 28),
                         fg="black")
        label.pack(pady=30)

        if result.is_draw:
            text = "Draw!"
        elif result.game_mode == GameMode.MULTI_PLAYER:
            text = "Player 1 Wins!" if result.winner == PLAYER_1 else "Player 2 Wins!"
        else:
            text = "You Win!" if result.winner == PLAYER_1 else "You Lose!"

        winner_label = tk.Label(self.root,
                                text=text,
                                font=("Arial", 22),
                                fg="red" if result.winner == PLAYER_1 else "yellow")
        winner_label.pack(pady=10)

        start_btn = tk.Button(self.root,
                                text="Start New Game",
                                font=("Arial", 18),
                                bg="white",
                                fg="black",
                                width=15,
                                height=2,
                                command=self.display_menu_page)
        start_btn.pack(pady=15)

        replay_btn = tk.Button(self.root,
                             text="Replay",
                             font=("Arial", 18),
                             bg="white",
                             fg="black",
                             width=15,
                             height=2,
                             command=self.restart)
        replay_btn.pack(pady=15)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def draw(self):
        self.root.mainloop()


if __name__ == "__main__":
    UILayer().draw()
