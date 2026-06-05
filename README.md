# 🏓 Pong — Classic Arcade in Python + Pygame

A clean, beginner-friendly implementation of the classic Pong arcade game built with Python and Pygame. Designed as a learning project and a polished GitHub portfolio piece.

---

## 📁 Project Structure

```
pong_game/
│
├── main.py              # Entry point — starts the app, owns the state machine
├── game.py              # Core gameplay loop (paddles, ball, scoring, pause)
├── menu.py              # Main menu + win screen UI
├── paddle.py            # Paddle class — movement, drawing, collision rect
├── ball.py              # Ball class — physics, bouncing, speed increase
├── scoreboard.py        # Score display + center dashed line
├── sound_manager.py     # Wraps pygame.mixer — loads & plays sound effects
├── settings.py          # ALL constants in one place (colors, speeds, sizes)
│
├── generate_sounds.py   # One-time script to generate placeholder .wav files
├── requirements.txt     # pip dependencies
│
└── assets/
    └── sounds/
        ├── paddle_hit.wav
        ├── wall_hit.wav
        ├── score.wav
        └── win.wav
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/pong-pygame.git
cd pong-pygame
```

### 2. (Recommended) Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate sound effects (run once)
```bash
python generate_sounds.py
```

### 5. Run the game
```bash
python main.py
```

---

## 🎮 Controls

| Action            | Player 1  | Player 2      |
|-------------------|-----------|---------------|
| Move Up           | `W`       | `↑` Arrow     |
| Move Down         | `S`       | `↓` Arrow     |
| Pause / Resume    | `P`       | `P`           |
| Back to Menu      | `Escape`  | `Escape`      |

---

## 🕹️ Features

- **Main menu** with mouse-hover buttons
- **Two paddles** with smooth keyboard controls
- **Physics-based ball** with angle variation on paddle hit
- **Increasing ball speed** on every paddle contact
- **Score tracking** — first to **7** wins
- **Pause feature** (press `P`)
- **Sound effects** for paddle hit, wall bounce, score, and win
- **Winning screen** with restart / main menu options
- **Retro CRT scanline** aesthetic
- **60 FPS** locked framerate
- **Glow effects** on paddles and ball

---

## 🏗️ Architecture Overview

```
main.py
  └─ state machine: "menu" → "game" → "win"

game.py  (state: "game")
  ├─ Paddle (x2)          ← paddle.py
  ├─ Ball                 ← ball.py
  ├─ Scoreboard           ← scoreboard.py
  └─ SoundManager         ← sound_manager.py

menu.py  (states: "menu", "win")
  └─ uses same screen surface as Game
```

**Game Loop (per frame):**
1. `_handle_events()` — keyboard, quit, pause toggle
2. `_update()` — move paddles → move ball → check collisions → check score
3. `_draw()` — fill background → scoreboard → paddles → ball → flip display

---

