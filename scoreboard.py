"""
scoreboard.py — Scoreboard rendering.

Draws the score display at the top of the screen and the dashed center line.
This class is purely visual — it reads scores from the paddles but never
modifies them.
"""

import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    FONT_LARGE, FONT_SMALL,
    WHITE, LIGHT_GRAY, NEON_GREEN, NEON_BLUE,
    DASH_HEIGHT, DASH_GAP
)


class Scoreboard:
    """
    Renders:
      - Player 1 score (left side)
      - Player 2 score (right side)
      - A dashed vertical center line
      - Optional "PAUSED" overlay text
    """

    def __init__(self):
        # The large score digits
        self.score_font  = pygame.font.SysFont("monospace", FONT_LARGE, bold=True)
        # Smaller label text ("PLAYER 1", "PLAYER 2")
        self.label_font  = pygame.font.SysFont("monospace", FONT_SMALL)

    # ── PUBLIC ────────────────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface, score_left: int, score_right: int,
             paused: bool = False):
        """
        Draw the full scoreboard.

        Args:
            screen      : the pygame surface to draw on
            score_left  : score for the left player (Player 1)
            score_right : score for the right player (Player 2)
            paused      : if True, draw a "PAUSED" banner
        """
        self._draw_center_line(screen)
        self._draw_scores(screen, score_left, score_right)

        if paused:
            self._draw_paused(screen)

    # ── PRIVATE ───────────────────────────────────────────────────────────────

    def _draw_center_line(self, screen: pygame.Surface):
        """
        Draw a vertical dashed line down the center of the screen.
        This is the classic Pong aesthetic.
        """
        x = WINDOW_WIDTH // 2
        y = 0
        while y < WINDOW_HEIGHT:
            pygame.draw.rect(
                screen,
                LIGHT_GRAY,
                (x - 2, y, 4, DASH_HEIGHT)
            )
            y += DASH_HEIGHT + DASH_GAP

    def _draw_scores(self, screen: pygame.Surface, score_left: int, score_right: int):
        """Render each player's score and label near the top."""
        quarter = WINDOW_WIDTH // 4

        # ── Left player (Player 1) ──────────────────────────────────────────
        # Score digit
        p1_score_surf = self.score_font.render(str(score_left), True, NEON_GREEN)
        p1_score_rect = p1_score_surf.get_rect(center=(quarter, 55))
        screen.blit(p1_score_surf, p1_score_rect)

        # Label
        p1_label_surf = self.label_font.render("P1  W/S", True, LIGHT_GRAY)
        p1_label_rect = p1_label_surf.get_rect(center=(quarter, 100))
        screen.blit(p1_label_surf, p1_label_rect)

        # ── Right player (Player 2) ─────────────────────────────────────────
        p2_score_surf = self.score_font.render(str(score_right), True, NEON_BLUE)
        p2_score_rect = p2_score_surf.get_rect(center=(quarter * 3, 55))
        screen.blit(p2_score_surf, p2_score_rect)

        p2_label_surf = self.label_font.render("P2  ↑/↓", True, LIGHT_GRAY)
        p2_label_rect = p2_label_surf.get_rect(center=(quarter * 3, 100))
        screen.blit(p2_label_surf, p2_label_rect)

    def _draw_paused(self, screen: pygame.Surface):
        """Semi-transparent overlay with PAUSED text."""
        # Dark translucent banner across the middle
        overlay = pygame.Surface((WINDOW_WIDTH, 80), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, WINDOW_HEIGHT // 2 - 40))

        pause_font = pygame.font.SysFont("monospace", 42, bold=True)
        pause_surf = pause_font.render("— PAUSED —  (P to resume)", True, WHITE)
        pause_rect = pause_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(pause_surf, pause_rect)
