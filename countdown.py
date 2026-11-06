"""Countdown to 19 November (Netherlands time, Europe/Amsterdam).
Big flip-clock style digits, updates every 250ms. tkinter, zero deps.
"""

import tkinter as tk
from datetime import datetime, timedelta, timezone

# 19 November 2026, 00:00:00 in the Netherlands.
# On that date the Netherlands is on CET (UTC+1) - DST ends late October.
TARGET = datetime(2026, 11, 19, 0, 0, 0,
                  tzinfo=timezone(timedelta(hours=1)))

BG = "#0d0d1a"
PANEL = "#17172b"
ACCENT = "#ffd166"
TEXT = "#e8e8f0"
MUTED = "#8f8fb0"


def digits_str(n, width=2):
    return str(n).zfill(width)


class Countdown(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Countdown to 19 November")
        self.configure(bg=BG)
        self.resizable(False, False)

        tk.Label(self, text="UNTIL 19 NOVEMBER",
                 font=("Consolas", 15, "bold"), fg=ACCENT, bg=BG
                 ).pack(pady=(26, 4))
        tk.Label(self, text="Netherlands time (CET)",
                 font=("Consolas", 11), fg=MUTED, bg=BG
                 ).pack()

        self.row = tk.Frame(self, bg=BG)
        self.row.pack(pady=18)

        self.labels = {}
        units = [("DAYS", 4), ("HOURS", 2), ("MINUTES", 2), ("SECONDS", 2)]
        for i, (name, w) in enumerate(units):
            cell = tk.Frame(self.row, bg=PANEL,
                            highlightbackground="#2a2a4a",
                            highlightthickness=1)
            cell.pack(side="left", padx=8)
            num = tk.Label(cell, text="0" * w,
                           font=("Consolas", 52, "bold"),
                           fg=TEXT, bg=PANEL, width=w)
            num.pack(padx=10, pady=(14, 0))
            tk.Label(cell, text=name, font=("Consolas", 10, "bold"),
                     fg=MUTED, bg=PANEL).pack(pady=(0, 10))
            if i < len(units) - 1:
                tk.Label(self.row, text=":", font=("Consolas", 36, "bold"),
                         fg=ACCENT, bg=BG).pack(side="left", padx=4)
            self.labels[name] = num

        # progress bar: fraction of the year elapsed toward target
        self.bar_bg = tk.Canvas(self, width=560, height=14, bg=PANEL,
                                highlightthickness=1,
                                highlightbackground="#2a2a4a")
        self.bar_bg.pack(pady=(10, 6))
        self.bar = self.bar_bg.create_rectangle(2, 2, 2, 12,
                                                fill=ACCENT, width=0)

        self.status = tk.Label(self, text="", font=("Consolas", 11),
                               fg=MUTED, bg=BG)
        self.status.pack(pady=(2, 20))

        self.after(250, self.tick)

    def tick(self):
        now = datetime.now(timezone.utc)
        remain = TARGET - now
        total = remain.total_seconds()

        if total <= 0:
            for name in self.labels:
                self.labels[name].config(text="0" * len(self.labels[name].cget("text")))
            self.labels["DAYS"].config(text="00")
            self.labels["HOURS"].config(text="00")
            self.labels["MINUTES"].config(text="00")
            self.labels["SECONDS"].config(text="00")
            self.status.config(text="IT'S 19 NOVEMBER!")
            self.after(1000, self.tick)
            return

        days = int(total // 86400)
        hours = int((total % 86400) // 3600)
        minutes = int((total % 3600) // 60)
        seconds = int(total % 60)

        self.labels["DAYS"].config(text=digits_str(days, 4))
        self.labels["HOURS"].config(text=digits_str(hours))
        self.labels["MINUTES"].config(text=digits_str(minutes))
        self.labels["SECONDS"].config(text=digits_str(seconds))

        # progress: from 1 Jan 2026 to target
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        span = (TARGET - start).total_seconds()
        frac = max(0.0, min(1.0, 1 - total / span))
        self.bar_bg.coords(self.bar, 2, 2, 2 + 556 * frac, 12)

        # extra context: also show exact target time
        local = TARGET.astimezone(timezone(timedelta(hours=1)))
        self.status.config(
            text=f"target: {local:%d %B %Y %H:%M} CET   ·   "
                 f"{total/86400:.1f} days left")

        self.after(250, self.tick)


if __name__ == "__main__":
    Countdown().mainloop()
