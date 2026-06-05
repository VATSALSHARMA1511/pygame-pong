"""
paddle.py — Paddle class.

Each player controls one Paddle instance.
The paddle knows about its own position, speed, and how to draw itself.
It does NOT know about the ball or scores — separation of concerns.
"""

import pygame
from settings import (
    PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED,
    WINDOW_HEIGHT, WHITE, NEON_GREEN, NEON_BLUE
)


class Paddle:
    """
    Represents a single player paddle.

    Attributes:
        x (int)           : horizontal position (stays fixed per player)
        y (float)         : vertical center of the paddle
        width (int)       : paddle width in pixels
        height (int)      : paddle height in pixels
        speed (int)       : pixels the paddle moves each frame
        color (tuple)     : RGB color
        rect (pygame.Rect): used for drawing and collision detection
        score (int)       : this player's current score
    """

    def __init__(self, x: int, color: tuple):
        """
        Args:
            x     : fixed horizontal position of the paddle
            color : RGB tuple for the paddle's color
        """
        self.x      = x
        self.y      = WINDOW_HEIGHT // 2    # start vertically centered
        self.width  = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed  = PADDLE_SPEED
        self.color  = color
        self.score  = 0

        # pygame.Rect is the standard collision/drawing rectangle.
        # We rebuild it every frame in update() so it always matches self.y
        self.rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )

    # ── MOVEMENT ──────────────────────────────────────────────────────────────

    def move_up(self):
        """Move the paddle upward, clamped to the top of the screen."""
        self.y -= self.speed
        self._clamp()

    def move_down(self):
        """Move the paddle downward, clamped to the bottom of the screen."""
        self.y += self.speed
        self._clamp()

    def _clamp(self):
        """
        Prevent the paddle from leaving the screen vertically.
        half_h keeps the calculation readable.
        """
        half_h = self.height // 2
        # Top boundary: paddle center must be at least half its height from top
        if self.y - half_h < 0:
            self.y = half_h
        # Bottom boundary: paddle center must be at least half its height from bottom
        if self.y + half_h > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - half_h

    # ── UPDATE ────────────────────────────────────────────────────────────────

    def update(self):
        """
        Sync the pygame.Rect to the current y position.
        Call this once per frame BEFORE drawing or collision checks.
        """
        self.rect.x = self.x - self.width // 2
        self.rect.y = int(self.y) - self.height // 2

    def reset_position(self):
        """Snap the paddle back to the vertical center (called after a point)."""
        self.y = WINDOW_HEIGHT // 2

    # ── DRAWING ───────────────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface):
        """
        Draw the paddle with a subtle glow effect.

        The glow is achieved by drawing a slightly larger, semi-transparent
        rectangle behind the paddle.  This is purely cosmetic.
        """
        # Glow layer: slightly bigger, translucent rect drawn to a temp surface
        glow_surf = pygame.Surface(
            (self.width + 8, self.height + 8), pygame.SRCALPHA
        )
        glow_color = (*self.color, 60)  # same color, but alpha = 60 (out of 255)
        pygame.draw.rect(
            glow_surf, glow_color,
            glow_surf.get_rect(), border_radius=4
        )
        screen.blit(
            glow_surf,
            (self.rect.x - 4, self.rect.y - 4)
        )

        # Main paddle body
        pygame.draw.rect(screen, self.color, self.rect, border_radius=4)
