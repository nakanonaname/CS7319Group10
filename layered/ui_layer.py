import tkinter as tk
import numpy as np
from game_session_layer import GameSessionLayer, GameMode, PLAYER_1, MoveResult

FONT = "Helvetica"

class UILayer(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4 - Layered")

        # menu page fields/components
        self.game_mode_var = None

        # game board fields/components
        self.canvas = None
        self.cells = None
        self.cell_size = 50
        self.cell_padding = 10
        self.player_turn_label = None

        self._game_session_layer = GameSessionLayer()

    def display_menu_page(self):
        """Display menu page with options to start a game"""

        self.clear_window()
        self.root.geometry("500x500")

        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=20)

        # Connect-4 title
        title_connect = tk.Label(title_frame,
                                 text="Connect",
                                 fg="red",
                                 font=(FONT, 24, "bold"))
        title_connect.pack(side=tk.LEFT)
        title_four = tk.Label(title_frame,
                              text="-4",
                              fg="yellow",
                              font=(FONT, 24, "bold"))
        title_four.pack(side=tk.LEFT)

        # Choose opponent radios
        label = tk.Label(self.root,
                         text="Choose your opponent:",
                         font=(FONT, 14))
        label.pack(pady=20)

        radio_frame = tk.Frame(self.root)
        radio_frame.pack(pady=10)

        self.game_mode_var = tk.StringVar(value="SINGLE_PLAYER")
        ai_radio_btn = tk.Radiobutton(radio_frame,
                                      text="Monte Carlo AI",
                                      variable=self.game_mode_var,
                                      value="SINGLE_PLAYER",
                                      font=(FONT, 12))
        ai_radio_btn.pack(anchor=tk.W, pady=5)
        multi_player_btn = tk.Radiobutton(radio_frame,
                                          text="2 Players",
                                          variable=self.game_mode_var,
                                          value="MULTIPLAYER",
                                          font=(FONT, 12))
        multi_player_btn.pack(anchor=tk.W, pady=5)

        start_btn = tk.Button(self.root,
                                 text="Start Game",
                                 font=(FONT, 14),
                                 command=self.handle_start_click)
        start_btn.pack(pady=20)

    def display_game_page(self, game_mode: GameMode):
        """display game board"""
        self.clear_window()

        # start session as player 1
        self._game_session_layer.start_session(game_mode=game_mode)

        self.root.geometry("670x400")
        self.root.minsize(670, 400)
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        main_container.grid_columnconfigure(0, weight=3, minsize=400)
        main_container.grid_columnconfigure(1, weight=1, minsize=200)
        main_container.grid_rowconfigure(0, weight=1)

        self.cells = np.zeros((7, 6), dtype=int)

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
                                   font=(FONT, 16),
                                   bg="white",
                                   width=12,
                                   height=1,
                                   command=self.display_menu_page)
        btn_start_game.pack(pady=10)

        btn_restart = tk.Button(menu_frame,
                                text="Restart Game",
                                font=(FONT, 16),
                                bg="white",
                                width=12,
                                height=1,
                                command=self.handle_restart_click)
        btn_restart.pack(pady=10)

        spacer = tk.Frame(menu_frame)
        spacer.pack(fill=tk.BOTH, expand=True)

        # show player turn indicator for multiplayer mode
        if game_mode == GameMode.MULTI_PLAYER:
            self.player_turn_label = tk.Label(
                menu_frame,
                text="Player Turn: Player 1",
                font=(FONT, 10),
                justify=tk.LEFT
            )
            self.player_turn_label.pack(side=tk.BOTTOM, pady=15)

        player_legend_yellow_text = tk.Label(
            menu_frame,
            text="Player 2" if self._game_session_layer.is_multiplayer else "Monte Carlo AI",
            font=(FONT, 10),
            fg="yellow",
            justify=tk.LEFT
        )
        player_legend_yellow_text.pack(side=tk.BOTTOM)

        player_legend_red_text = tk.Label(
            menu_frame,
            text="Player 1",
            font=(FONT, 10),
            highlightcolor="red",
            fg="red",
            justify=tk.LEFT
        )
        player_legend_red_text.pack(side=tk.BOTTOM)

        self.display_board_widget()

    def display_end_page(self, result: MoveResult):
        """Display end page for a given result"""
        self.clear_window()
        self.cells = np.zeros((7, 6), dtype=int)

        label = tk.Label(self.root,
                         text="Game Over",
                         font=(FONT, 28),
                         fg="black")
        label.pack(pady=30)

        if result.is_draw:
            text = "Draw!"
        elif self._game_session_layer.is_multiplayer:
            if result.winner == PLAYER_1:
                text = "Player 1 Wins!"
            else:
                text = "Player 2 Wins!"
        else:
            if result.winner == PLAYER_1:
                text = "You Win!"
            else:
                text = "You Lose!"

        winner_label = tk.Label(self.root,
                                text=text,
                                font=(FONT, 22),
                                fg="red" if result.winner == PLAYER_1 else "yellow")
        winner_label.pack(pady=10)

        start_btn = tk.Button(self.root,
                                text="Start New Game",
                                font=(FONT, 18),
                                bg="white",
                                fg="black",
                                width=15,
                                height=2,
                                command=self.display_menu_page)
        start_btn.pack(pady=15)

        replay_btn = tk.Button(self.root,
                             text="Replay",
                             font=(FONT, 18),
                             bg="white",
                             fg="black",
                             width=15,
                             height=2,
                             command=self.handle_restart_click)
        replay_btn.pack(pady=15)

    def display_board_widget(self):
        """Display board view, render cells"""

        for x in range(len(self.cells[0])):
            for y in range(len(self.cells)):
                x1 = y * (self.cell_size + self.cell_padding) + 10
                y1 = x * (self.cell_size + self.cell_padding) + 10
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.cells[y, x] = self.canvas.create_oval(x1, y1, x2, y2, fill="white")

    def handle_start_click(self):
        """handle start click event
            transform radio button TextVar to GameMode enum"""
        game_mode_text = self.game_mode_var.get()
        game_mode = GameMode.SINGLE_PLAYER if game_mode_text == "SINGLE_PLAYER" else GameMode.MULTI_PLAYER

        self.display_game_page(game_mode=game_mode)

    def handle_restart_click(self):
        self._game_session_layer.restart_session()
        self.display_game_page(self._game_session_layer.game_mode)

    def handle_cell_click(self, event):
        """Handle game cell clicked event"""

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

    def update_player_turn_label(self):
        """Generate turn label"""
        current = "Player 1" if self._game_session_layer.current_player == PLAYER_1 else "Player 2"
        self.player_turn_label.config(text=f"Player Turn: {current}")

    def clear_window(self):
        """Destroy existing widgets in tkinter root"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def draw(self):
        """Present menu and start game loop"""
        self.display_menu_page()
        self.root.mainloop()
