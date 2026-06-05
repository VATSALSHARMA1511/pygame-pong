"""
menu.py — Main menu and winning screen rendering.

Menu is separate from Game intentionally:
  - Game handles gameplay
  - Menu handles UI screens

Both use the same screen surface so there's only ever one window.
"""

import pygame
import sys
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    BLACK, WHITE, LIGHT_GRAY, NEON_GREEN, NEON_BLUE, YELLOW, GRAY,
    FONT_LARGE, FONT_MEDIUM, FONT_SMALL, FONT_TINY
)


class Menu:
    """
    Handles the main menu screen and the post-game winning screen.

    Methods:
        run()               → show main menu, return next state
        show_win_screen()   → show winner announcement, return next state
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock  = pygame.time.Clock()

        # Fonts
        self.title_font  = pygame.font.SysFont("monospace", FONT_LARGE,  bold=True)
        self.medium_font = pygame.font.SysFont("monospace", FONT_MEDIUM, bold=True)
        self.small_font  = pygame.font.SysFont("monospace", FONT_SMALL)
        self.tiny_font   = pygame.font.SysFont("monospace", FONT_TINY)

        # Button hover state tracking
        self._hovered = None

    # ── MAIN MENU ─────────────────────────────────────────────────────────────

    def run(self) -> str:
        """
        Display the main menu and block until the player makes a choice.

        Returns:
            "game" → player pressed Start
            (exits the process) → player pressed Exit
        """
        # Button definitions: (label, action_string, y_position)
        buttons = [
            ("▶  START GAME", "game", WINDOW_HEIGHT // 2 + 20),
            ("✕  EXIT",        "exit", WINDOW_HEIGHT // 2 + 100),
        ]

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return "game"
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for label, action, btn_y in buttons:
                        btn_rect = self._button_rect(btn_y)
                        if btn_rect.collidepoint(mouse_pos):
                            if action == "exit":
                                pygame.quit(); sys.exit()
                            return action

            self._draw_menu(buttons, mouse_pos)
            self.clock.tick(FPS)

    # ── WIN SCREEN ────────────────────────────────────────────────────────────

    def show_win_screen(self, winner: str) -> str:
        """
        Display the winning screen and block until the player chooses.

        Args:
            winner : "Player 1" or "Player 2"

        Returns:
            "game" → player chose Restart
            (exits) → player chose Exit
        """
        winner_color = NEON_GREEN if winner == "Player 1" else NEON_BLUE
        buttons = [
            ("↺  PLAY AGAIN", "game", WINDOW_HEIGHT // 2 + 80),
            ("⌂  MAIN MENU",  "menu", WINDOW_HEIGHT // 2 + 160),
        ]

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_r:
                        return "game"
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for label, action, btn_y in buttons:
                        if self._button_rect(btn_y).collidepoint(mouse_pos):
                            return action

            self._draw_win_screen(winner, winner_color, buttons, mouse_pos)
            self.clock.tick(FPS)

    # ── DRAWING HELPERS ───────────────────────────────────────────────────────

    def _draw_menu(self, buttons, mouse_pos):
        """Render the main menu frame."""
        self.screen.fill(BLACK)

        # Subtle scanline texture
        self._draw_scanlines()

        # Title
        title_surf = self.title_font.render("P O N G", True, WHITE)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120))
        self.screen.blit(title_surf, title_rect)

        # Subtitle
        sub_surf = self.tiny_font.render(
            "Two-player classic  •  First to 7 wins", True, LIGHT_GRAY
        )
        sub_rect = sub_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        self.screen.blit(sub_surf, sub_rect)

        # Controls hint
        controls = [
            "Player 1 : W / S keys",
            "Player 2 : ↑ / ↓ arrows",
            "Pause    : P key",
        ]
        for i, line in enumerate(controls):
            surf = self.tiny_font.render(line, True, GRAY)
            rect = surf.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100 + i * 26)
            )
            self.screen.blit(surf, rect)

        # Buttons
        for label, action, btn_y in buttons:
            hover = self._button_rect(btn_y).collidepoint(mouse_pos)
            self._draw_button(label, btn_y, hover)

        pygame.display.flip()

    def _draw_win_screen(self, winner, winner_color, buttons, mouse_pos):
        """Render the winning screen frame."""
        self.screen.fill(BLACK)
        self._draw_scanlines()

        # "WINNER!" heading
        win_surf = self.title_font.render("WINNER!", True, YELLOW)
        win_rect = win_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 110))
        self.screen.blit(win_surf, win_rect)

        # Player name
        name_surf = self.medium_font.render(winner, True, winner_color)
        name_rect = name_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        self.screen.blit(name_surf, name_rect)

        # Buttons
        for label, action, btn_y in buttons:
            hover = self._button_rect(btn_y).collidepoint(mouse_pos)
            self._draw_button(label, btn_y, hover)

        pygame.display.flip()

    def _draw_button(self, label: str, center_y: int, hovered: bool):
        """
        Draw a single menu button.

        Args:
            label    : button text
            center_y : vertical center of the button
            hovered  : True if the mouse is over this button
        """
        btn_rect = self._button_rect(center_y)

        # Background fill
        bg_color   = GRAY if not hovered else (70, 70, 70)
        text_color = WHITE if not hovered else NEON_GREEN

        pygame.draw.rect(self.screen, bg_color,  btn_rect, border_radius=8)
        pygame.draw.rect(self.screen, LIGHT_GRAY, btn_rect, width=2, border_radius=8)

        # Label text
        surf = self.small_font.render(label, True, text_color)
        rect = surf.get_rect(center=btn_rect.center)
        self.screen.blit(surf, rect)

    def _button_rect(self, center_y: int) -> pygame.Rect:
        """Return the Rect for a button centered at center_y."""
        btn_w, btn_h = 300, 55
        return pygame.Rect(
            WINDOW_WIDTH // 2 - btn_w // 2,
            center_y - btn_h // 2,
            btn_w,
            btn_h
        )

    def _draw_scanlines(self):
        """
        Draw very faint horizontal lines across the entire screen for a
        retro CRT effect.  This is cheap: one Surface created per draw call
        but it's small-ish and the alpha is very low.
        """
        line_surf = pygame.Surface((WINDOW_WIDTH, 2), pygame.SRCALPHA)
        line_surf.fill((255, 255, 255, 8))    # nearly invisible white
        y = 0
        while y < WINDOW_HEIGHT:
            self.screen.blit(line_surf, (0, y))
            y += 4   # every 4 pixels draws 2px line + 2px gap
