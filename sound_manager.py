"""
sound_manager.py — Sound effect handler.

Wraps pygame.mixer so the rest of the code never needs to worry about
whether sound files exist or whether loading failed.

BEGINNER TIP:
    Always guard sound loading in a try/except.  If a .wav file is missing
    the game should still run — just silently.  Never let a missing asset
    crash the game.
"""

import pygame
from settings import SOUND_PADDLE_HIT, SOUND_WALL_HIT, SOUND_SCORE, SOUND_WIN


class SoundManager:
    """
    Loads and plays all game sound effects.

    If a sound file is missing or fails to load, the corresponding slot
    is set to None and play() calls on it are silently skipped.
    """

    def __init__(self):
        self.sounds: dict[str, pygame.mixer.Sound | None] = {
            "paddle" : self._load(SOUND_PADDLE_HIT),
            "wall"   : self._load(SOUND_WALL_HIT),
            "score"  : self._load(SOUND_SCORE),
            "win"    : self._load(SOUND_WIN),
        }

    # ── PUBLIC ────────────────────────────────────────────────────────────────

    def play(self, name: str):
        """
        Play a named sound effect.

        Args:
            name : key in self.sounds — "paddle", "wall", "score", or "win"
        """
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def set_volume(self, volume: float):
        """
        Set the master volume for all sounds.

        Args:
            volume : float between 0.0 (silent) and 1.0 (full)
        """
        for sound in self.sounds.values():
            if sound is not None:
                sound.set_volume(volume)

    # ── PRIVATE ───────────────────────────────────────────────────────────────

    @staticmethod
    def _load(path: str) -> pygame.mixer.Sound | None:
        """
        Attempt to load a sound file.  Returns None on failure.
        """
        try:
            return pygame.mixer.Sound(path)
        except (pygame.error, FileNotFoundError):
            # Sound file is missing — game continues without it
            print(f"[SoundManager] Could not load: {path}  (game will run silently)")
            return None
