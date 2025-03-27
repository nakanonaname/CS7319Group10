import tkinter as tk

class WinnerDisplay(tk.Frame):
    def __init__(self, parent, winner, start_new_game_callback, replay_callback):
        super().__init__(parent, padx=30, pady=30)
        self.pack()

        winner_text = "Player 1 - Yellow wins!" if winner == 1 else "Player 2 - Red wins!" if winner == 2 else "It's a draw!"
        self.label = tk.Label(self, text=winner_text, font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.new_game_button = tk.Button(self, text="Start New Game", command=start_new_game_callback)
        self.new_game_button.pack(side=tk.LEFT, padx=10)

        self.replay_button = tk.Button(self, text="Replay", command=lambda: replay_callback())
        self.replay_button.pack(side=tk.RIGHT, padx=10)
