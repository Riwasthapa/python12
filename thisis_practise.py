# click_target.py
import tkinter as tk
import random
import time

WIDTH, HEIGHT = 600, 400
RADIUS = 25
START_TIME = 30         # seconds
SPEED_INCREASE = 0.9    # multiply interval by this each hit (lower -> faster)

class ClickGame:
    def __init__(self, master):
        self.master = master
        master.title("Click the Target!")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.score = 0
        self.time_left = START_TIME
        self.interval = 1000   # ms between moves
        self.running = False

        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text="", font=("Helvetica", 14))
        self.time_text = self.canvas.create_text(WIDTH-10, 10, anchor="ne", text="", font=("Helvetica", 14))

        self.target = None
        self.target_pos = (WIDTH//2, HEIGHT//2)

        # Buttons
        btn_frame = tk.Frame(master)
        btn_frame.pack(fill="x")
        self.start_btn = tk.Button(btn_frame, text="Start", command=self.start_game)
        self.start_btn.pack(side="left", padx=8, pady=6)
        self.reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_game)
        self.reset_btn.pack(side="left", padx=8, pady=6)

        # Bind clicks
        self.canvas.bind("<Button-1>", self.on_click)

        self.update_ui()
        self.spawn_target()

    def spawn_target(self):
        x = random.randint(RADIUS, WIDTH - RADIUS)
        y = random.randint(RADIUS + 20, HEIGHT - RADIUS)  # leave room for UI
        self.target_pos = (x, y)
        if self.target:
            self.canvas.delete(self.target)
        self.target = self.canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill="red", outline="black")

    def on_click(self, event):
        if not self.running: 
            return
        x, y = event.x, event.y
        tx, ty = self.target_pos
        if (x - tx) ** 2 + (y - ty) ** 2 <= RADIUS ** 2:
            self.score += 1
            # make it harder
            self.interval = max(100, int(self.interval * SPEED_INCREASE))
            self.spawn_target()

    def tick(self):
        if not self.running:
            return
        self.time_left -= 1
        if self.time_left <= 0:
            self.end_game()
            return
        self.spawn_target()                     # move target every tick
        self.update_ui()
        self.master.after(self.interval, self.tick)

    def start_game(self):
        if self.running:
            return
        self.running = True
        self.score = 0
        self.time_left = START_TIME
        self.interval = 1000
        self.update_ui()
        # schedule ticks: we want a tick every 1 second for the timer, but movement governed by interval
        self.master.after(1000, self._timer_tick)
        self.master.after(self.interval, self.tick)

    def _timer_tick(self):
        if not self.running:
            return
        self.time_left -= 1
        if self.time_left <= 0:
            self.end_game()
            return
        self.update_ui()
        self.master.after(1000, self._timer_tick)

    def end_game(self):
        self.running = False
        self.update_ui()
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text=f"Time's up!\nScore: {self.score}", font=("Helvetica", 24), fill="blue")

    def reset_game(self):
        self.running = False
        self.score = 0
        self.time_left = START_TIME
        self.interval = 1000
        self.canvas.delete("all")
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text="", font=("Helvetica", 14))
        self.time_text = self.canvas.create_text(WIDTH-10, 10, anchor="ne", text="", font=("Helvetica", 14))
        self.target = None
        self.spawn_target()
        self.update_ui()

    def update_ui(self):
        self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfigure(self.time_text, text=f"Time: {self.time_left}s")

if __name__ == "__main__":
    root = tk.Tk()
    game = ClickGame(root)
    root.mainloop()
