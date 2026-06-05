"""
settings.py — Central configuration file for all game constants.

BEGINNER TIP:
    Keeping all "magic numbers" here means you can tweak the entire
    game's feel just by editing this one file. Never scatter raw numbers
    throughout your code — name everything.
"""

# ── WINDOW ────────────────────────────────────────────────────────────────────
WINDOW_WIDTH  = 900
WINDOW_HEIGHT = 600
WINDOW_TITLE  = "Pong — Classic Arcade"
FPS           = 60          # Frames per second cap

# ── COLORS  (R, G, B) ─────────────────────────────────────────────────────────
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GRAY       = (40,  40,  40)
LIGHT_GRAY = (180, 180, 180)
NEON_GREEN = (57,  255, 20)
NEON_BLUE  = (0,   200, 255)
NEON_RED   = (255, 50,  50)
YELLOW     = (255, 220, 0)

# ── PADDLE ────────────────────────────────────────────────────────────────────
PADDLE_WIDTH   = 14
PADDLE_HEIGHT  = 90
PADDLE_SPEED   = 6          # pixels per frame
PADDLE_MARGIN  = 30         # distance from left/right edges

# ── BALL ──────────────────────────────────────────────────────────────────────
BALL_SIZE           = 14    # pixel width/height (it's a square)
BALL_INITIAL_SPEED  = 5     # starting speed (pixels per frame)
BALL_MAX_SPEED      = 14    # speed ceiling so the game doesn't get unplayable
BALL_SPEED_INCREMENT = 0.4  # added to speed on every paddle hit

# ── SCORING ───────────────────────────────────────────────────────────────────
WINNING_SCORE = 7           # first to this score wins

# ── FONT SIZES ────────────────────────────────────────────────────────────────
FONT_LARGE  = 72
FONT_MEDIUM = 48
FONT_SMALL  = 28
FONT_TINY   = 20

# ── SOUND PATHS ───────────────────────────────────────────────────────────────
# These paths are relative to the project root (where main.py lives).
# Place your .wav files inside assets/sounds/.
SOUND_PADDLE_HIT = "assets/sounds/paddle_hit.wav"
SOUND_WALL_HIT   = "assets/sounds/wall_hit.wav"
SOUND_SCORE      = "assets/sounds/score.wav"
SOUND_WIN        = "assets/sounds/win.wav"

# ── CENTER LINE ───────────────────────────────────────────────────────────────
DASH_HEIGHT = 12            # height of each dash segment on the center line
DASH_GAP    = 8             # gap between dash segments
