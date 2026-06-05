"""
main.py — Entry point of the Pong game.

This file is responsible for:
- Initializing Pygame
- Running the main game state machine (menu → game → win screen)
- Controlling the overall game loop

HOW IT CONNECTS:
    main.py → creates Game() → which uses Paddle, Ball, Scoreboard, SoundManager
"""

import pygame
import sys
from settings import FPS, WINDOW_TITLE
from game import Game
from menu import Menu


def main():
    """
    Application entry point.
    Initialize pygame, create the window, and run the game state machine.
    """
    pygame.init()
    pygame.mixer.init()  # Initialize the audio system

    # Create the game and menu instances
    # They share the same screen surface so everything draws to one window
    game = Game()
    menu = Menu(game.screen)

    clock = pygame.time.Clock()

    # ── STATE MACHINE ──────────────────────────────────────────────────────────
    # The game has three states:
    #   "menu"   → show main menu, wait for player to press Start or Exit
    #   "game"   → run the actual Pong gameplay
    #   "win"    → show the winning screen, offer restart
    state = "menu"

    while True:
        # Each state returns the NEXT state so we transition cleanly
        if state == "menu":
            state = menu.run()          # blocks until player picks an option

        elif state == "game":
            state = game.run()          # blocks until someone wins or quits

        elif state == "win":
            state = menu.show_win_screen(game.winner)  # blocks until restart/exit

        else:
            # Safety valve — should never reach here
            break

        clock.tick(FPS)  # Cap the outer loop (inner loops have their own ticks)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
