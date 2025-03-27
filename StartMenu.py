import tkinter as tk

class StartMenu(tk.Frame):
    def __init__(self, parent, start_game_callback):
        super().__init__(parent)
        self.parent = parent
        self.start_game_callback = start_game_callback

        self.pack(padx=30, pady=30)

        self.title_frame = tk.Frame(self)
        self.title_frame.pack(pady=20)

        self.title_connect = tk.Label(self.title_frame, text="Connect", fg="red", font=("Helvetica", 24, "bold"))
        self.title_connect.pack(side=tk.LEFT)

        self.title_four = tk.Label(self.title_frame, text="-4", fg="yellow", font=("Helvetica", 24, "bold"))
        self.title_four.pack(side=tk.LEFT)

        self.label = tk.Label(self, text="Choose your opponent:", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.opponent_var = tk.StringVar(value="Monte Carlo AI")
        self.opponents = ["Monte Carlo AI", "2 Players"]

        self.radio_frame = tk.Frame(self)
        self.radio_frame.pack(pady=10)

        for opponent in self.opponents:
            radio_button = tk.Radiobutton(self.radio_frame, text=opponent, variable=self.opponent_var, value=opponent, font=("Helvetica", 12))
            radio_button.pack(anchor=tk.W, pady=5)

        self.start_button = tk.Button(self, text="Start Game", font=("Helvetica", 14), command=self.on_start)
        self.start_button.pack(pady=20)

    def on_start(self):
        chosen_opponent = self.opponent_var.get()
        self.start_game_callback(chosen_opponent)
