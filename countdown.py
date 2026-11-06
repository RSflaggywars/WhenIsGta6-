"""Countdown to 19 November (Netherlands time, Europe/Amsterdam).
Minimal flip-clock style. tkinter, zero deps.
"""

import tkinter as tk
from datetime import datetime, timedelta, timezone

TARGET = datetime(2026, 11, 19, 0, 0, 0,
                  tzinfo=timezone(timedelta(hours=1)))  # CET = UTC+1

BG = "#0e0e13"
TEXT = "#f2f2f5"
DIM = "#55555f"
LINE = "#26262e"
ACCENT = "#e8e8ee"

FONT_NUM = ("Segoe UI", 64)
FONT_UNIT = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)


def z(n, w=2):
    return str(n).zfill(w)


class Countdown(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("19 November")
        self.configure(bg=BG)
        self.resizable(False, False)

        # header
        tk.Label(self, text="19  N  O  V  E  M  B  E  R",
                 font=FONT_LABEL, fg=DIM, bg=BG
                 ).pack(pady=(34, 0))
        tk.Label(self, text="AMSTERDAM · CET",
                 font=FONT_SMALL, fg="#3a3a44", bg=BG
                 ).pack()

        # digits row
        self.row = tk.Frame(self, bg=BG)
        self.row.pack(pady=26)

        self.labels = {}
        units = [("DAYS", 4), ("HRS", 2), ("MIN", 2), ("SEC", 2)]
        for i, (name, w) in enumerate(units):
            cell = tk.Frame(self.row, bg=BG)
            cell.pack(side="left")
            num = tk.Label(cell, text="0" * w, font=FONT_NUM,
                           fg=TEXT, bg=BG)
            num.pack()
            tk.Label(cell, text=name, font=FONT_UNIT, fg=DIM, bg=BG
                     ).pack(pady=(2, 0))
            self.labels[name] = num
            if i < len(units) - 1:
                tk.Label(self.row, text="·", font=("Segoe UI", 40),
                         fg="#33333d", bg=BG).pack(side="left",
                                                   padx=14, pady=30)

        # hairline progress
        self.canvas = tk.Canvas(self, width=520, height=2, bg=BG,
                                highlightthickness=0)
        self.canvas.pack(pady=(18, 0))
        self.canvas.create_rectangle(0, 0, 520, 2, fill=LINE,
                                     outline="")
        self.fill = self.canvas.create_rectangle(0, 0, 0, 2,
                                                 fill=TEXT, outline="")

        self.status = tk.Label(self, text="", font=FONT_SMALL,
                               fg="#3a3a44", bg=BG)
        self.status.pack(pady=14)

        self.after(250, self.tick)

    def tick(self):
        total = (TARGET - datetime.now(timezone.utc)).total_seconds()

        if total <= 0:
            for name, w in (("DAYS", 4), ("HRS", 2), ("MIN", 2), ("SEC", 2)):
                self.labels[name].config(text="0" * w)
            self.status.config(text="it is 19 november")
            self.after(1000, self.tick)
            return

        days = int(total // 86400)
        hours = int((total % 86400) // 3600)
        minutes = int((total % 3600) // 60)
        seconds = int(total % 60)

        self.labels["DAYS"].config(text=z(days, 4))
        self.labels["HRS"].config(text=z(hours))
        self.labels["MIN"].config(text=z(minutes))
        self.labels["SEC"].config(text=z(seconds))

        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        frac = max(0.0, min(1.0, 1 - total / (TARGET - start).total_seconds()))
        self.canvas.coords(self.fill, 0, 0, 520 * frac, 2)

        self.status.config(text=f"{total / 86400:.2f} days remaining")
        self.after(250, self.tick)


if __name__ == "__main__":
    Countdown().mainloop()
