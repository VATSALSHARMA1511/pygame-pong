"""
game.py — Core gameplay loop.

This is the heart of the application.  Game is responsible for:
  1. Creating the window/screen
  2. Owning all game objects (paddles, ball, scoreboard, sounds)
  3. Reading keyboard input and routing it to the right paddle
  4. Running the game loop (update → draw → flip)
  5. Detecting the win condition and returning a state signal to main.py

STATE RETURNS:
    "menu"  → player pressed Escape  (go back to main menu)
    "win"   → a player reached WINNING_SCORE  (go to win screen)
"""

import pygame
import time
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS,
    BLACK, GRAY, NEON_GREEN, NEON_BLUE, WHITE,
    PADDLE_MARGIN, WINNING_SCORE
)
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
from sound_manager import SoundManager


# Short pause (seconds) after a point before the ball resets
SCORE_PAUSE_DURATION = 1.2


class Game:
    """
    Owns and orchestrates all gameplay objects.

    The window/screen is created once here and shared with Menu so the
    whole application renders to a single window.
    """

    def __init__(self):
        # ── Window ────────────────────────────────────────────────────────────
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        self.clock  = pygame.time.Clock()

        # ── Game objects ──────────────────────────────────────────────────────
        # Player 1 is on the LEFT, Player 2 is on the RIGHT
        self.paddle_left  = Paddle(x=PADDLE_MARGIN, color=NEON_GREEN)
        self.paddle_right = Paddle(x=WINDOW_WIDTH - PADDLE_MARGIN, color=NEON_BLUE)
        self.ball         = Ball()
        self.scoreboard   = Scoreboard()
        self.sounds       = SoundManager()

        # ── State ─────────────────────────────────────────────────────────────
        self.paused  = False
        self.winner  = ""   # set when someone wins ("Player 1" / "Player 2")

    # ── PUBLIC: main loop ─────────────────────────────────────────────────────

    def run(self) -> str:
        """
        Run the game loop until the game ends.

        Returns:
            "menu" if the player presses Escape
            "win"  if a player reaches the winning score
        """
        self._reset_game()  # fresh state every time we enter gameplay

        while True:
            # 1. Handle events (quit, keyboard presses)
            result = self._handle_events()
            if result:
                return result   # "menu" on Escape / "win" on win condition

            # 2. Update game objects (only when not paused)
            if not self.paused:
                self._update()

            # 3. Draw everything
            self._draw()

            # 4. Cap the frame rate
            self.clock.tick(FPS)

    # ── PRIVATE: reset ────────────────────────────────────────────────────────

    def _reset_game(self):
        """Reset scores, positions, and ball for a brand-new game."""
        self.paddle_left.score  = 0
        self.paddle_right.score = 0
        self.paddle_left.reset_position()
        self.paddle_right.reset_position()
        self.ball.reset()
        self.paused = False
        self.winner = ""

    # ── PRIVATE: events ───────────────────────────────────────────────────────

    def _handle_events(self) -> str | None:
        """
        Process the event queue.

        Returns a state string to transition to, or None to keep playing.
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                import sys; sys.exit()

            if event.type == pygame.KEYDOWN:
                # Pause / unpause
                if event.key == pygame.K_p:
                    self.paused = not self.paused

                # Back to menu
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        return None  # nothing to transition

    # ── PRIVATE: update ───────────────────────────────────────────────────────

    def _update(self) -> str | None:
        """
        Update game logic for one frame.
        Handles paddle movement, ball physics, and scoring.
        """
        # ── Paddle input  ─────────────────────────────────────────────────────
        # pygame.key.get_pressed() checks which keys are HELD DOWN this frame.
        # This is different from KEYDOWN events (which fire once on press).
        # For smooth movement, always use get_pressed().
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:      self.paddle_left.move_up()
        if keys[pygame.K_s]:      self.paddle_left.move_down()
        if keys[pygame.K_UP]:     self.paddle_right.move_up()
        if keys[pygame.K_DOWN]:   self.paddle_right.move_down()

        # Sync rects after movement
        self.paddle_left.update()
        self.paddle_right.update()

        # ── Ball physics ──────────────────────────────────────────────────────
        event = self.ball.update(self.paddle_left, self.paddle_right)

        if event == "wall":
            self.sounds.play("wall")

        elif event == "paddle":
            self.sounds.play("paddle")

        elif event == "score":
            self._handle_score()

    def _handle_score(self):
        """Award a point, check for win, then reset the ball."""
        self.sounds.play("score")

        if self.ball.scored == "left":
            # Ball exited the LEFT side → right player (P2) scores
            self.paddle_right.score += 1
        else:
            # Ball exited the RIGHT side → left player (P1) scores
            self.paddle_left.score += 1

        # Draw the current state so the player sees the updated score
        # during the pause
        self._draw()
        pygame.display.flip()
        time.sleep(SCORE_PAUSE_DURATION)

        # Check win condition
        if self.paddle_left.score >= WINNING_SCORE:
            self.winner = "Player 1"
            self.sounds.play("win")
            # Brief pause so the win sound can start before we leave
            time.sleep(0.4)
            # We need to signal the win — but we're inside _update().
            # We set a flag and the outer loop in run() will catch it.
            self._signal_win = True
            return

        if self.paddle_right.score >= WINNING_SCORE:
            self.winner = "Player 2"
            self.sounds.play("win")
            time.sleep(0.4)
            self._signal_win = True
            return

        # Nobody won yet — reset positions and ball
        self.paddle_left.reset_position()
        self.paddle_right.reset_position()
        self.ball.reset()

    # ── PRIVATE: draw ─────────────────────────────────────────────────────────

    def _draw(self):
        """Render all game objects to the screen."""
        # Background
        self.screen.fill(BLACK)

        # Center line + scores (scoreboard draws the dashed line too)
        self.scoreboard.draw(
            self.screen,
            self.paddle_left.score,
            self.paddle_right.score,
            paused=self.paused
        )

        # Game objects
        self.paddle_left.draw(self.screen)
        self.paddle_right.draw(self.screen)
        self.ball.draw(self.screen)

        pygame.display.flip()

    # ── Override run() to handle _signal_win ──────────────────────────────────
    # We patch the run() method slightly so the win signal propagates cleanly.

    def run(self) -> str:  # noqa: F811  (intentional re-def)
        self._reset_game()
        self._signal_win = False

        while True:
            result = self._handle_events()
            if result:
                return result

            if not self.paused:
                self._update()
                if self._signal_win:
                    return "win"

            self._draw()
            self.clock.tick(FPS)
