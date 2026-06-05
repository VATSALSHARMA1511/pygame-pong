"""
ball.py — Ball class.

Handles all ball physics:
  - Movement (velocity vector)
  - Wall bouncing (top / bottom)
  - Paddle collision with angle variation
  - Speed increase on each paddle hit
  - Scoring detection (ball exits left or right)

The ball does NOT modify scores directly — it signals a score event and
the Game class handles it.  Single responsibility principle.
"""

import pygame
import math
import random
from settings import (
    BALL_SIZE, BALL_INITIAL_SPEED, BALL_MAX_SPEED, BALL_SPEED_INCREMENT,
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, YELLOW
)


class Ball:
    """
    Represents the pong ball.

    The ball moves using a velocity vector (vx, vy).
    Speed is the scalar magnitude: speed = sqrt(vx² + vy²)

    Attributes:
        rect   (pygame.Rect) : position and size for drawing/collision
        vx     (float)       : horizontal velocity (pixels/frame)
        vy     (float)       : vertical velocity   (pixels/frame)
        speed  (float)       : current scalar speed
        scored (str | None)  : set to "left" or "right" when ball exits a side
    """

    def __init__(self):
        self.size  = BALL_SIZE
        self.rect  = pygame.Rect(0, 0, self.size, self.size)
        self.speed = BALL_INITIAL_SPEED
        self.vx    = 0.0
        self.vy    = 0.0
        self.scored: str | None = None   # which side conceded ("left"/"right")
        self.reset()

    # ── RESET ─────────────────────────────────────────────────────────────────

    def reset(self):
        """
        Re-center the ball and launch it in a random direction.
        Called at game start and after each point is scored.
        """
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.speed  = BALL_INITIAL_SPEED
        self.scored = None

        # Pick a random launch angle between -35° and +35°,
        # then randomly choose left or right direction.
        angle_deg = random.uniform(-35, 35)
        angle_rad = math.radians(angle_deg)

        direction = random.choice([-1, 1])   # -1 = left, 1 = right
        self.vx = direction * self.speed * math.cos(angle_rad)
        self.vy = self.speed * math.sin(angle_rad)

    # ── UPDATE ────────────────────────────────────────────────────────────────

    def update(self, paddle_left, paddle_right):
        """
        Advance the ball one frame.

        Args:
            paddle_left  (Paddle) : left player's paddle
            paddle_right (Paddle) : right player's paddle
        """
        # Move the ball
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        # ── Top / bottom wall bounce ──────────────────────────────────────────
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy = abs(self.vy)          # force downward
            return "wall"                   # signal for sound

        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.vy = -abs(self.vy)         # force upward
            return "wall"

        # ── Left / right exit → score ─────────────────────────────────────────
        if self.rect.right < 0:
            self.scored = "left"            # right player scores
            return "score"

        if self.rect.left > WINDOW_WIDTH:
            self.scored = "right"           # left player scores
            return "score"

        # ── Paddle collisions ─────────────────────────────────────────────────
        if self._check_paddle_collision(paddle_left, side="left"):
            return "paddle"

        if self._check_paddle_collision(paddle_right, side="right"):
            return "paddle"

        return None   # nothing notable happened this frame

    # ── PRIVATE: PADDLE COLLISION ─────────────────────────────────────────────

    def _check_paddle_collision(self, paddle, side: str) -> bool:
        """
        Check and resolve a collision between the ball and a paddle.

        Angle variation:
            Where on the paddle the ball hits determines the bounce angle.
            Hitting the center = mostly horizontal.
            Hitting the edges  = steeper angle (more vy).
        This makes the game far more skillful and interesting.

        Returns True if a collision occurred this frame.
        """
        if not self.rect.colliderect(paddle.rect):
            return False

        # Calculate where on the paddle the ball hit: -1 (top) to +1 (bottom)
        paddle_center = paddle.rect.centery
        hit_pos       = self.rect.centery - paddle_center
        normalized    = hit_pos / (paddle.height / 2)   # range [-1, 1]
        normalized    = max(-1.0, min(1.0, normalized))  # clamp just in case

        # Max bounce angle = 60 degrees
        bounce_angle = normalized * math.radians(60)

        # Increase speed (but don't exceed the cap)
        self.speed = min(self.speed + BALL_SPEED_INCREMENT, BALL_MAX_SPEED)

        # Rebuild velocity from angle and speed
        if side == "left":
            # Ball should now go RIGHT
            self.vx = self.speed * math.cos(bounce_angle)
            self.rect.left = paddle.rect.right + 1   # prevent sticking
        else:
            # Ball should now go LEFT
            self.vx = -self.speed * math.cos(bounce_angle)
            self.rect.right = paddle.rect.left - 1

        self.vy = self.speed * math.sin(bounce_angle)
        return True

    # ── DRAWING ───────────────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface):
        """Draw the ball with a subtle glow."""
        # Glow
        glow_surf = pygame.Surface(
            (self.size + 10, self.size + 10), pygame.SRCALPHA
        )
        pygame.draw.rect(
            glow_surf, (*YELLOW, 50),
            glow_surf.get_rect(), border_radius=3
        )
        screen.blit(glow_surf, (self.rect.x - 5, self.rect.y - 5))

        # Ball body
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=3)
