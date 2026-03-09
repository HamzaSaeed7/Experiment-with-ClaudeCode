import tkinter as tk
import random
import math

# --- Dark-theme palette ---
BG           = "#1e1e2e"
PANEL        = "#2a2a3e"
BTN          = "#3d3d5c"
BTN_HOV      = "#4e4e72"
BTN_DIM      = "#2d2d44"
FG           = "#cdd6f4"
FG_DIM       = "#6c7086"

GOLD         = "#ffd966"
GOLD_EDGE    = "#b8860b"
GOLD_DARK    = "#7a5c00"
GOLD_SHADOW  = "#2a1f00"
SILVER       = "#c0c0c0"
SILVER_EDGE  = "#808080"
SILVER_DARK  = "#505050"
SILVER_SHADOW = "#1a1a1a"


class CoinFlipApp:
    def __init__(self, root):
        self.root = root
        root.title("Coin Toss")
        root.configure(bg=BG)
        root.resizable(False, False)

        # State
        self.current_face = "Heads"
        self.animating = False
        self.heads = 0
        self.tails = 0

        # Layout constants
        self.width  = 320
        self.height = 320
        self.radius = 90
        self.center = (self.width // 2, self.height // 2)

        # Canvas
        self.canvas = tk.Canvas(
            root, width=self.width, height=self.height,
            bg=BG, highlightthickness=0
        )
        self.canvas.pack(padx=16, pady=(16, 4))

        # Result label
        self.result_label = tk.Label(
            root, text="— Ready —",
            font=("Helvetica", 14, "bold"), bg=BG, fg=FG_DIM
        )
        self.result_label.pack(pady=(0, 8))

        # Stats row
        stats_frame = tk.Frame(root, bg=PANEL, padx=12, pady=6)
        stats_frame.pack(fill=tk.X, padx=16, pady=(0, 10))

        self.heads_lbl = tk.Label(
            stats_frame, text="H: 0",
            font=("Helvetica", 11, "bold"), bg=PANEL, fg=GOLD
        )
        self.heads_lbl.pack(side=tk.LEFT, padx=10)

        self.tails_lbl = tk.Label(
            stats_frame, text="T: 0",
            font=("Helvetica", 11, "bold"), bg=PANEL, fg=SILVER
        )
        self.tails_lbl.pack(side=tk.LEFT, padx=10)

        self.total_lbl = tk.Label(
            stats_frame, text="/ 0",
            font=("Helvetica", 11), bg=PANEL, fg=FG_DIM
        )
        self.total_lbl.pack(side=tk.RIGHT, padx=10)

        # Buttons
        btn_frame = tk.Frame(root, bg=BG)
        btn_frame.pack(pady=(0, 4))

        self.flip_btn = self._make_btn(
            btn_frame, "Flip  [Space]", self.flip,
            font=("Helvetica", 12, "bold"), padx=18, pady=8
        )
        self.flip_btn.pack(side=tk.LEFT, padx=8)

        self._make_btn(btn_frame, "Reset", self._reset_stats).pack(side=tk.LEFT, padx=4)
        self._make_btn(btn_frame, "Quit", root.quit).pack(side=tk.LEFT, padx=4)

        # Hint label
        tk.Label(
            root, text="Space / Enter to flip",
            font=("Helvetica", 9), bg=BG, fg=FG_DIM
        ).pack(pady=(0, 14))

        # Keybindings
        root.bind("<space>",  lambda e: self.flip())
        root.bind("<Return>", lambda e: self.flip())

        # Initial draw
        self.draw_coin(1.0, self.current_face)

    # --- Helpers ---

    def _make_btn(self, parent, text, command,
                  font=("Helvetica", 10), padx=10, pady=5):
        btn = tk.Button(
            parent, text=text, command=command,
            font=font, bg=BTN, fg=FG,
            activebackground=BTN_HOV, activeforeground=FG,
            relief=tk.FLAT, cursor="hand2",
            padx=padx, pady=pady, bd=0
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOV) if btn["state"] != "disabled" else None)
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN     ) if btn["state"] != "disabled" else None)
        return btn

    def _update_stats(self, face):
        if face == "Heads":
            self.heads += 1
        else:
            self.tails += 1
        self.heads_lbl.config(text=f"H: {self.heads}")
        self.tails_lbl.config(text=f"T: {self.tails}")
        self.total_lbl.config(text=f"/ {self.heads + self.tails}")

    def _reset_stats(self):
        self.heads = 0
        self.tails = 0
        self.heads_lbl.config(text="H: 0")
        self.tails_lbl.config(text="T: 0")
        self.total_lbl.config(text="/ 0")
        self.result_label.config(text="— Ready —", fg=FG_DIM)
        self.root.title("Coin Toss")

    @staticmethod
    def _ease(t):
        """Ease-in-out cubic: slow start → fast middle → slow landing."""
        if t < 0.5:
            return 4 * t * t * t
        p = 2 * t - 2
        return 1 + p * p * p / 2

    # --- Drawing ---

    def draw_coin(self, scale_x=1.0, face="Heads"):
        self.canvas.delete("all")
        cx, cy = self.center
        rx = max(1, int(self.radius * abs(scale_x)))
        ry = self.radius

        if face == "Heads":
            shadow_c, edge_c, face_c, text_c = GOLD_SHADOW, GOLD_DARK, GOLD, GOLD_DARK
        else:
            shadow_c, edge_c, face_c, text_c = SILVER_SHADOW, SILVER_DARK, SILVER, SILVER_DARK

        # Drop shadow (offset by 6 px)
        sd = 6
        self.canvas.create_oval(
            cx - rx + sd, cy - ry + sd, cx + rx + sd, cy + ry + sd,
            fill=shadow_c, outline=""
        )
        # Edge strip — thickness illusion (offset down 4 px)
        self.canvas.create_oval(
            cx - rx, cy - ry + 4, cx + rx, cy + ry + 4,
            fill=edge_c, outline=""
        )
        # Main face oval
        self.canvas.create_oval(
            cx - rx, cy - ry, cx + rx, cy + ry,
            fill=face_c, outline=edge_c, width=2
        )
        # Inner decorative ring (72 % of radius)
        ir = 0.72
        self.canvas.create_oval(
            cx - int(rx * ir), cy - int(ry * ir),
            cx + int(rx * ir), cy + int(ry * ir),
            fill="", outline=edge_c, width=1
        )
        # Face text — scales with apparent width
        font_size = max(8, int(28 * (0.5 + 0.5 * abs(scale_x))))
        self.canvas.create_text(
            cx, cy, text=face,
            font=("Helvetica", font_size, "bold"), fill=text_c
        )

    # --- Animation ---

    def flip(self):
        if self.animating:
            return
        self.animating = True
        self.flip_btn.config(state="disabled", bg=BTN_DIM, cursor="arrow")

        frames   = 50
        duration = 1300  # ms
        flips    = 6
        final    = random.choice(["Heads", "Tails"])

        self._animate_frame(0, frames, flips, final, duration / frames)

    def _animate_frame(self, i, frames, flips, final, delay_ms):
        if i >= frames:
            self.draw_coin(1.0, final)
            self.current_face = final
            self.animating = False
            self.flip_btn.config(state="normal", bg=BTN, cursor="hand2")

            color = GOLD if final == "Heads" else SILVER
            self.result_label.config(
                text="HEADS!" if final == "Heads" else "TAILS!",
                fg=color
            )
            self.root.title(f"Coin Toss — {final}")
            self._update_stats(final)
            return

        eased      = self._ease(i / frames)
        cosv       = math.cos(eased * flips * math.pi)
        scale      = 0.15 + 0.85 * abs(cosv)
        half_flips = int(eased * flips * 2)
        face       = "Heads" if (half_flips % 2 == 0) else "Tails"

        self.draw_coin(scale, face)
        self.root.after(
            int(delay_ms),
            lambda: self._animate_frame(i + 1, frames, flips, final, delay_ms)
        )


def main():
    root = tk.Tk()
    app = CoinFlipApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
