import tkinter as tk
import random

class StartMenu(tk.Frame):
    def __init__(self, parent, start_game_callback, open_color_selector_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.start_game_callback = start_game_callback
        self.open_color_selector_callback = open_color_selector_callback

        self.canvas = tk.Canvas(self, width=500, height=500, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.particles = []
        self.animate_particles()

        self.title_label = tk.Label(self.parent, text="Connect-4", font=("Helvetica", 28, "bold"),
                                    fg="white", bg="black")
        self.canvas.create_window(250, 60, window=self.title_label)

        self.label = tk.Label(self.parent, text="Mode:", font=("Helvetica", 14),
                              fg="white", bg="black")
        self.canvas.create_window(250, 130, window=self.label)

        self.opponent_var = tk.StringVar(value="Monte Carlo AI")
        self.radio_frame = tk.Frame(self.parent, bg="black")

        radio1 = tk.Radiobutton(self.radio_frame, text="Monte Carlo AI", variable=self.opponent_var,
                                value="Monte Carlo AI", font=("Helvetica", 12),
                                bg="black", fg="white", selectcolor="gray")
        radio2 = tk.Radiobutton(self.radio_frame, text="2 Players", variable=self.opponent_var,
                                value="2 Players", font=("Helvetica", 12),
                                bg="black", fg="white", selectcolor="gray")

        radio1.pack(anchor=tk.W, pady=5)
        radio2.pack(anchor=tk.W, pady=5)
        self.canvas.create_window(250, 180, window=self.radio_frame)

        self.start_button = tk.Button(self.parent,
                                      text="Start",
                                      font=("Helvetica", 14),
                                      command=self.on_start)
        self.canvas.create_window(250, 260, window=self.start_button)

    def animate_particles(self):
        self.canvas.delete("particles")

        if random.random() < 0.3:
            x = random.randint(0, 500)
            size = random.randint(2, 4)
            color = random.choice(["#5555ff", "#7777ff", "#9999ff"])
            self.particles.append([x, 0, size, color])

        updated_particles = []
        for x, y, r, color in self.particles:
            y += 2
            if y < 500:
                self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                        fill=color, outline="", tags="particles")
                updated_particles.append([x, y, r, color])

        self.particles = updated_particles
        self.after(30, self.animate_particles)

    def on_start(self):
        opponent = self.opponent_var.get()
        if self.open_color_selector_callback:
            self.open_color_selector_callback(opponent)
        else:
            self.start_game_callback(opponent)
