import tkinter as tk

class Connect4UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")
        self.root.geometry("700x800")
        self.root.configure(bg="white")  # 设置背景颜色为白色
        self.show_start_page()

    def show_start_page(self):
        self.clear_window()

        label = tk.Label(self.root, text="Connect 4", font=("Arial", 28), fg="black", bg="white")
        label.pack(pady=30)

        btn_two_players = tk.Button(self.root, text="Multiplayer", font=("Arial", 18), bg="white", fg="black",
                                    width=15, height=2, command=self.start_two_player_game)
        btn_two_players.pack(pady=15)

        btn_ai = tk.Button(self.root, text="AI Player", font=("Arial", 18), bg="white", fg="black",
                           width=15, height=2, command=self.start_ai_game)
        btn_ai.pack(pady=15)

        btn_exit = tk.Button(self.root, text="Exit", font=("Arial", 18), bg="white", fg="black",
                             width=15, height=2, command=self.root.quit)
        btn_exit.pack(pady=30)

    def start_two_player_game(self):
        self.show_game_ui(mode="Multiplayer")

    def start_ai_game(self):
        self.show_game_ui(mode="AI Player")

    def show_game_ui(self, mode):
        self.clear_window()

        menu_frame = tk.Frame(self.root, bg="white")
        menu_frame.pack(pady=10)

        btn_restart = tk.Button(menu_frame, text="Restart", font=("Arial", 16), bg="white", fg="black",
                                width=12, height=1, command=self.show_start_page)
        btn_restart.pack(side="left", padx=40)

        btn_exit = tk.Button(menu_frame, text="Exit", font=("Arial", 16), bg="white", fg="black",
                             width=12, height=1, command=self.root.quit)
        btn_exit.pack(side="left", padx=40)

        # 标题
        label = tk.Label(self.root, text=f"{mode} - In Game", font=("Arial", 22), fg="black", bg="white")
        label.pack(pady=20)

        # 绘制棋盘
        self.canvas = tk.Canvas(self.root, width=700, height=600, bg="white", highlightthickness=0)
        self.canvas.pack()

        self.draw_board()

        # 模拟游戏结束按钮（仅用于展示 UI）
        btn_end = tk.Button(self.root, text="End Game", font=("Arial", 18), bg="white", fg="black",
                            width=15, height=2, command=self.show_end_page)
        btn_end.pack(pady=30)

    def draw_board(self):
        for row in range(6):
            for col in range(7):
                x1, y1 = col * 100 + 10, row * 100 + 10
                x2, y2 = x1 + 80, y1 + 80
                self.canvas.create_oval(x1, y1, x2, y2, fill="gray", outline="white")  # 空棋子为灰色，边框为白色

    def show_end_page(self):
        self.clear_window()

        label = tk.Label(self.root, text="Game Over！", font=("Arial", 28), fg="black", bg="white")
        label.pack(pady=30)

        winner_label = tk.Label(self.root, text="Player X Wins!", font=("Arial", 22), fg="black", bg="white")
        winner_label.pack(pady=10)

        btn_restart = tk.Button(self.root, text="Back", font=("Arial", 18), bg="white", fg="black",
                                width=15, height=2, command=self.show_start_page)
        btn_restart.pack(pady=15)

        btn_exit = tk.Button(self.root, text="Exit", font=("Arial", 18), bg="white", fg="black",
                             width=15, height=2, command=self.root.quit)
        btn_exit.pack(pady=15)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Connect4UI(root)
    root.mainloop()
