"""
generate_sounds.py — Generates simple placeholder .wav sound effects.

Run this ONCE before running the game:
    python generate_sounds.py

It creates the four required .wav files in assets/sounds/ using only
Python's built-in 'wave' and 'struct' modules — no extra dependencies.

HOW IT WORKS:
    We generate raw PCM audio data (sine waves, noise, etc.) and pack it
    into the .wav file format manually.  This is a great beginner exercise
    in understanding how audio data works.

Each sound:
    paddle_hit  → short high beep (like the classic Pong bleep)
    wall_hit    → lower, softer thud
    score       → descending two-tone chime
    win         → short ascending fanfare
"""

import wave
import struct
import math
import os


# ── Configuration ─────────────────────────────────────────────────────────────
SAMPLE_RATE  = 44100   # 44.1 kHz — CD quality
NUM_CHANNELS = 1       # Mono
SAMPLE_WIDTH = 2       # 16-bit (2 bytes per sample)

OUTPUT_DIR = "assets/sounds"


def generate_sine(
    frequency: float,
    duration: float,
    amplitude: float = 0.5,
    fade_out: bool = True
) -> list[int]:
    """
    Generate raw PCM samples for a sine wave tone.

    Args:
        frequency : pitch in Hz
        duration  : length in seconds
        amplitude : loudness 0.0–1.0
        fade_out  : apply a linear fade to reduce clicking at end

    Returns:
        List of signed 16-bit integer samples.
    """
    num_samples = int(SAMPLE_RATE * duration)
    samples     = []

    for i in range(num_samples):
        t     = i / SAMPLE_RATE
        value = amplitude * math.sin(2 * math.pi * frequency * t)

        # Linear fade-out over the last 20% of samples
        if fade_out:
            fade_start = int(num_samples * 0.8)
            if i >= fade_start:
                fade_factor = 1.0 - (i - fade_start) / (num_samples - fade_start)
                value *= fade_factor

        # Scale to 16-bit range [-32767, 32767]
        samples.append(int(value * 32767))

    return samples


def save_wav(filename: str, samples: list[int]):
    """Write a list of 16-bit PCM samples to a .wav file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with wave.open(filename, "w") as wf:
        wf.setnchannels(NUM_CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(SAMPLE_RATE)
        # Pack each sample as a signed short (little-endian)
        packed = struct.pack(f"<{len(samples)}h", *samples)
        wf.writeframes(packed)

    print(f"  ✓  Created {filename}")


def create_paddle_hit():
    """Short, punchy high beep — classic Pong bleep."""
    samples = generate_sine(frequency=480, duration=0.07, amplitude=0.6)
    save_wav(f"{OUTPUT_DIR}/paddle_hit.wav", samples)


def create_wall_hit():
    """Lower, softer thud for the wall bounce."""
    samples = generate_sine(frequency=220, duration=0.08, amplitude=0.4)
    save_wav(f"{OUTPUT_DIR}/wall_hit.wav", samples)


def create_score():
    """
    Descending two-tone chime when a point is scored.
    We concatenate two different tones.
    """
    note1 = generate_sine(frequency=660, duration=0.12, amplitude=0.5)
    note2 = generate_sine(frequency=440, duration=0.18, amplitude=0.5)
    samples = note1 + note2
    save_wav(f"{OUTPUT_DIR}/score.wav", samples)


def create_win():
    """
    Ascending four-note fanfare for the winning moment.
    C4 → E4 → G4 → C5
    """
    notes = [
        generate_sine(261.63, 0.12, 0.5),   # C4
        generate_sine(329.63, 0.12, 0.5),   # E4
        generate_sine(392.00, 0.12, 0.5),   # G4
        generate_sine(523.25, 0.30, 0.5),   # C5  (held longer)
    ]
    samples = []
    for note in notes:
        samples.extend(note)
    save_wav(f"{OUTPUT_DIR}/win.wav", samples)


if __name__ == "__main__":
    print(f"\nGenerating sound effects in '{OUTPUT_DIR}/'...\n")
    create_paddle_hit()
    create_wall_hit()
    create_score()
    create_win()
    print("\nAll sounds generated successfully!")
    print("You can now run:  python main.py\n")
