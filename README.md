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

## 🚀 Future Improvements

### Add an AI Opponent
Replace Player 2's keyboard input with a simple tracking algorithm:

```python
# In game.py _update(), replace arrow-key block with:
if self.ball.vx > 0:  # ball moving toward AI
    if self.paddle_right.rect.centery < self.ball.rect.centery - 5:
        self.paddle_right.move_down()
    elif self.paddle_right.rect.centery > self.ball.rect.centery + 5:
        self.paddle_right.move_up()
# Add a reaction_delay and position error for difficulty levels
```

### Convert to an Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# Output: dist/main.exe (Windows) or dist/main (macOS/Linux)
```

### Add Background Music
```python
pygame.mixer.music.load("assets/sounds/background.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)  # -1 = loop forever
```

### Add Online Multiplayer
Use Python's `socket` module:
- One player acts as **server** (binds to a port, waits for connection)
- Other player acts as **client** (connects to server's IP)
- Each frame: send your paddle Y → receive opponent's Y
- Libraries to explore: `socket`, `asyncio`, or the higher-level `pygame-network`

### More Ideas
- Power-ups (speed boost, paddle size change)
- Difficulty modes (Easy / Medium / Hard AI)
- Particle effects on paddle hit
- High score persistence (`json` file or `sqlite3`)
- Mobile touch controls

---

## 🐛 Common Beginner Mistakes (Avoided Here)

| Mistake | What We Do Instead |
|---------|-------------------|
| Hardcoding numbers everywhere | All constants live in `settings.py` |
| Putting all code in one file | Separate modules per responsibility |
| Using `KEYDOWN` for movement | Use `key.get_pressed()` for smooth hold |
| No sound error handling | `SoundManager` silently skips missing files |
| Forgetting `pygame.display.flip()` | Called once per frame in `_draw()` |
| Infinite speed ball | `BALL_MAX_SPEED` cap in `settings.py` |

---

## 📄 License

MIT — free to use, modify, and distribute.
