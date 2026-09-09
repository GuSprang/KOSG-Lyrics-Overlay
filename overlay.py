import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from spotify_client import play_pause, next_track, prev_track

# Palette
TRANSPARENT = "#010101"
BG          = "#0f0004"
BAR_COLOR   = "#3e001d"
LINE_COLOR  = "#8e004b"
ACCENT      = "#e91e8c"
TEXT_ON     = "#ffffff"
TEXT_OFF    = "#5a2a6a"
BTN_IDLE    = "#ffb1c8"
BTN_HOVER   = "#ff5c8a"

WIDTH    = 320
HEIGHT   = 220
RADIUS   = 16
TOPBAR_H = 26
CTRL_H   = 38

SS = 4  # supersampling: desenha 4x maior, depois reduz -> antialiasing

FONT_TRACK = ("Segoe UI", 9, "bold")
FONT_BIG   = ("Oswald", 15, "bold")
FONT_SMALL = ("Oswald", 10)
FONT_ICON  = ("Segoe UI Symbol", 12)

def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def render_panel():
    """Desenha o painel inteiro (fundo + topbar + controles) com antialiasing."""
    W, H = WIDTH * SS, HEIGHT * SS
    bg_rgb    = _hex_to_rgb(TRANSPARENT)
    trans_bg  = Image.new("RGB", (W, H), bg_rgb)

    flat = Image.new("RGB", (W, H), _hex_to_rgb(BG))
    draw = ImageDraw.Draw(flat)
    draw.rectangle([0, 0, W, TOPBAR_H * SS], fill=_hex_to_rgb(BAR_COLOR))
    draw.rectangle([0, H - CTRL_H * SS, W, H], fill=_hex_to_rgb(BAR_COLOR))
    draw.rectangle([0, TOPBAR_H * SS - SS, W, TOPBAR_H * SS], fill=_hex_to_rgb(LINE_COLOR))
    draw.rectangle([0, H - CTRL_H * SS, W, H - CTRL_H * SS + SS], fill=_hex_to_rgb(LINE_COLOR))

    mask = Image.new("L", (W, H), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, W - 1, H - 1], radius=RADIUS * SS, fill=255)

    composited = Image.composite(flat, trans_bg, mask)
    final = composited.resize((WIDTH, HEIGHT), Image.LANCZOS)
    return ImageTk.PhotoImage(final)


def render_circle(diameter, color, bg_color):
    D = diameter * SS
    flat = Image.new("RGB", (D, D), _hex_to_rgb(bg_color))
    draw = ImageDraw.Draw(flat)
    draw.ellipse([0, 0, D - 1, D - 1], fill=_hex_to_rgb(color))
    final = flat.resize((diameter, diameter), Image.LANCZOS)
    return ImageTk.PhotoImage(final)


class LyricsOverlay:
    def _heartbeat(self):
        self.root.update()
        self.root.after(100, self._heartbeat)

    def __init__(self, sp):
        self.sp       = sp
        self._lines   = []
        self._index   = -1
        self._playing = True
        self._drag_x  = None
        self._drag_y  = None
        self._images  = []  # guarda referência das PhotoImage (senão o garbage collector apaga)

        self.root = tk.Tk()
        self._setup_window()
        self._build_ui()
        self._build_controls()
        self._bind_drag()
        self._heartbeat()

    # ── Janela ────────────────────────────────────────────
    def _setup_window(self):
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", TRANSPARENT)
        self.root.configure(bg=TRANSPARENT)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = sw - WIDTH - 20
        y  = sh - HEIGHT - 60
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    # ── UI ────────────────────────────────────────────────
    def _build_ui(self):
        self.cv = tk.Canvas(
            self.root, width=WIDTH, height=HEIGHT,
            bg=TRANSPARENT, highlightthickness=0
        )
        self.cv.pack()

        panel_img = render_panel()
        self._images.append(panel_img)
        self.cv.create_image(0, 0, anchor="nw", image=panel_img)

        self._build_topbar()
        self._build_lyrics()
        self._build_controls()

    def _build_topbar(self):
        self.track_id = self.cv.create_text(
            14, TOPBAR_H // 2, anchor="w",
            text="Nada tocando...",
            fill=ACCENT, font=FONT_TRACK
        )
        close_id = self.cv.create_text(
            WIDTH - 14, TOPBAR_H // 2, anchor="e",
            text="✕", fill=TEXT_OFF, font=("Segoe UI", 10)
        )
        self.cv.tag_bind(close_id, "<Button-1>", lambda e: self.root.destroy())
        self.cv.tag_bind(close_id, "<Enter>",
                         lambda e: self.cv.itemconfig(close_id, fill="#ff4488"))
        self.cv.tag_bind(close_id, "<Leave>",
                         lambda e: self.cv.itemconfig(close_id, fill=TEXT_OFF))

    def _build_lyrics(self):
        cx = WIDTH // 2
        self.lrc_prev = self.cv.create_text(
            cx, 75, anchor="center", justify="center",
            text="", fill=TEXT_OFF,
            font=FONT_SMALL, width=WIDTH - 30
        )
        self.lrc_curr = self.cv.create_text(
            cx, 110, anchor="center", justify="center",
            text="♪  aguardando música...",
            fill=TEXT_ON, font=FONT_BIG, width=WIDTH - 30
        )
        self.lrc_next = self.cv.create_text(
            cx, 145, anchor="center", justify="center",
            text="", fill=TEXT_OFF,
            font=FONT_SMALL, width=WIDTH - 30
        )

    def _build_controls(self):
        btn_y = HEIGHT - (CTRL_H // 2)
        cx    = WIDTH // 2

        # (posição x, diâmetro, ícone, comando)
        specs = [
            (cx - 42, 24, "⏮", self._prev),
            (cx,      30, "⏸", self._play_pause),
            (cx + 42, 24, "⏭", self._next),
        ]

        for x, d, icon, cmd in specs:
            idle_img  = render_circle(d, BTN_IDLE, BAR_COLOR)
            hover_img = render_circle(d, BTN_HOVER, BAR_COLOR)
            self._images.extend([idle_img, hover_img])

            img_id = self.cv.create_image(x, btn_y, image=idle_img)
            txt_id = self.cv.create_text(
                x, btn_y - 1, anchor="center",
                text=icon, fill="#3e001d", font=FONT_ICON
            )

            def on_enter(e, i=img_id, h=hover_img):
                self.cv.itemconfig(i, image=h)

            def on_leave(e, i=img_id, idle=idle_img):
                self.cv.itemconfig(i, image=idle)

            for item in (img_id, txt_id):
                self.cv.tag_bind(item, "<Button-1>", lambda e, c=cmd: c())
                self.cv.tag_bind(item, "<Enter>", on_enter)
                self.cv.tag_bind(item, "<Leave>", on_leave)

            if icon == "⏸":
                self._play_txt = txt_id

    # ── Drag ──────────────────────────────────────────────
    def _bind_drag(self):
        self.cv.bind("<ButtonPress-1>", self._drag_start)
        self.cv.bind("<B1-Motion>",     self._drag_move)

    def _drag_start(self, event):
        if event.y < TOPBAR_H:
            self._drag_x = event.x_root - self.root.winfo_x()
            self._drag_y = event.y_root - self.root.winfo_y()
        else:
            self._drag_x = None

    def _drag_move(self, event):
        if self._drag_x is not None:
            x = event.x_root - self._drag_x
            y = event.y_root - self._drag_y
            self.root.geometry(f"+{x}+{y}")

    # ── Métodos públicos ───────────────────────────────────
    def set_track(self, artist, title):
        self.root.after(0, lambda: self.cv.itemconfig(
            self.track_id, text=f"{artist} — {title}"
        ))

    def set_lyrics(self, lines):
        def _update():
            self._lines = lines
            self._index = -1
            self.cv.itemconfig(self.lrc_prev, text="")
            self.cv.itemconfig(self.lrc_curr, text="♪  carregando...")
            self.cv.itemconfig(self.lrc_next, text="")
        self.root.after(0, _update)

    def highlight_line(self, index):
        def _update():
            if index == self._index or not self._lines:
                return
            self._index = index
            lines = self._lines
            prev_text = lines[index-1][1] if index > 0 else ""
            curr_text = lines[index][1] if index < len(lines) else ""
            next_text = lines[index+1][1] if index+1 < len(lines) else ""
            self.cv.itemconfig(self.lrc_prev, text=prev_text)
            self.cv.itemconfig(self.lrc_curr, text=curr_text)
            self.cv.itemconfig(self.lrc_next, text=next_text)
        self.root.after(0, _update)

    # ── Controles ─────────────────────────────────────────
    def _prev(self):
        try: prev_track(self.sp)
        except: pass

    def _play_pause(self):
        try:
            play_pause(self.sp)
            self._playing = not self._playing
            self.cv.itemconfig(
                self._play_txt,
                text="⏸" if self._playing else "▶"
            )
        except Exception as e:
            print(f"erro play_pause: {e}")

    def _next(self):
        try: next_track(self.sp)
        except: pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = LyricsOverlay(None)
    app.set_lyrics([
        (0,     "When I find myself in times of trouble"),
        (5000,  "Mother Mary comes to me"),
        (10000, "Speaking words of wisdom"),
        (15000, "Let it be"),
        (20000, "And in my hour of darkness"),
    ])
    app.highlight_line(2)
    app.run()