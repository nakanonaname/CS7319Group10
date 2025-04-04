import tkinter as tk
import numpy as np
from game_session_layer import GameSessionLayer, GameMode, PLAYER_1, MoveResult
import random
from tkinter import colorchooser
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

        self.particles = []
        self.canvas_bg = None

        self.animate_particles()

        self._game_session_layer = GameSessionLayer()

    def animate_particles(self):
        if not self.canvas:
            self.root.after(50, self.animate_particles)
            return

        self.canvas.delete("particles")

        if random.random() < 0.3:
            x = random.randint(0, 400)
            size = random.randint(1, 3)
            color = random.choice(["#6666ff", "#8888ff", "#9999ff"])
            self.particles.append([x, 0, size, color])

        updated_particles = []
        for x, y, r, color in self.particles:
            y += 2
            if y < 400:
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline='', tags="particles")
                updated_particles.append([x, y, r, color])
        self.particles = updated_particles

        self.root.after(30, self.animate_particles)

    def animate_piece_drop(self, x, y, player, delay=30):
        color1 = self.player1_color if hasattr(self, "player1_color") else "red"
        color2 = self.player2_color if hasattr(self, "player2_color") else "yellow"
        fill = color1 if player == PLAYER_1 else color2

        for i in range(y + 1):
            if i > 0:
                self.canvas.itemconfig(self.cells[x, i - 1], fill=self.board_color)
            self.canvas.itemconfig(self.cells[x, i], fill=fill)
            self.canvas.update()
            self.root.after(delay)

    def display_menu_page(self):

        self.clear_window()
        self.root.geometry("500x500")

        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.animate_particles()

        title = tk.Label(self.root,
                         text="Connect-4",
                         fg="white",
                         bg="black",
                         font=(FONT, 28, "bold"))
        self.canvas.create_window(250, 60, window=title)

        label = tk.Label(self.root,
                         text="Mode:",
                         font=(FONT, 14),
                         fg="white",
                         bg="black")
        self.canvas.create_window(250, 130, window=label)

        self.game_mode_var = tk.StringVar(value="SINGLE_PLAYER")

        radio_frame = tk.Frame(self.root, bg="black")
        ai_radio_btn = tk.Radiobutton(radio_frame,
                                      text="Monte Carlo AI",
                                      variable=self.game_mode_var,
                                      value="SINGLE_PLAYER",
                                      font=(FONT, 12),
                                      fg="white",
                                      bg="black",
                                      selectcolor="gray")
        ai_radio_btn.pack(anchor=tk.W, pady=5)

        multi_radio_btn = tk.Radiobutton(radio_frame,
                                         text="2 Players",
                                         variable=self.game_mode_var,
                                         value="MULTIPLAYER",
                                         font=(FONT, 12),
                                         fg="white",
                                         bg="black",
                                         selectcolor="gray")
        multi_radio_btn.pack(anchor=tk.W, pady=5)

        self.canvas.create_window(250, 180, window=radio_frame)

        start_btn = tk.Button(self.root,
                              text="Start",
                              font=(FONT, 14),
                              command=self.display_color_selector)
        self.canvas.create_window(250, 260, window=start_btn)

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

        bg_color = self.background_color if hasattr(self, "background_color") else "blue"
        self.canvas = tk.Canvas(game_frame, width=400, height=400, bg=bg_color)

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

    def display_color_selector(self):
        self.clear_window()

        self.canvas = tk.Canvas(self.root, width=500, height=400, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.animate_particles()

        # 初始化颜色（默认）
        self.player1_color = "#ff3333"
        self.player2_color = "#3333ff"
        self.board_color = "#f0f0f0"
        self.background_color = "#000000"

        def choose_color(title, var_name):
            color = colorchooser.askcolor(title=title)[1]
            if color:
                setattr(self, var_name, color)
                buttons[var_name].configure(bg=color)

        buttons = {}

        buttons["player1_color"] = tk.Button(self.root, text="player 1 color", bg=self.player1_color,
                                             command=lambda: choose_color("player 1 color", "player1_color"))
        self.canvas.create_window(250, 80, window=buttons["player1_color"])

        buttons["player2_color"] = tk.Button(self.root, text="player 2 color", bg=self.player2_color,
                                             command=lambda: choose_color("player 2 color", "player2_color"))
        self.canvas.create_window(250, 130, window=buttons["player2_color"])

        buttons["board_color"] = tk.Button(self.root, text="board color", bg=self.board_color,
                                           command=lambda: choose_color("board color", "board_color"))
        self.canvas.create_window(250, 180, window=buttons["board_color"])

        buttons["background_color"] = tk.Button(self.root, text="background color", bg=self.background_color,
                                                command=lambda: choose_color("background color", "background_color"))
        self.canvas.create_window(250, 230, window=buttons["background_color"])

        def start_game():
            game_mode_text = self.game_mode_var.get() if hasattr(self, "game_mode_var") else "SINGLE_PLAYER"
            game_mode = GameMode.SINGLE_PLAYER if game_mode_text == "SINGLE_PLAYER" else GameMode.MULTI_PLAYER
            self.display_game_page(game_mode=game_mode)

        start_game_btn = tk.Button(self.root, text="start", font=(FONT, 14), command=start_game)
        self.canvas.create_window(250, 300, window=start_game_btn)
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
        board_color = self.board_color if hasattr(self, "board_color") else "white"
        for x in range(len(self.cells[0])):
            for y in range(len(self.cells)):
                x1 = y * (self.cell_size + self.cell_padding) + 10
                y1 = x * (self.cell_size + self.cell_padding) + 10
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.cells[y, x] = self.canvas.create_oval(x1, y1, x2, y2, fill=board_color)

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
                self.animate_piece_drop(x, y, player)

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
