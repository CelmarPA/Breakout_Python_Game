import pygame
import os

class SoundManager:
    """
    Manages sound effects for the game using pygame's mixer module.
    Loads and plays predefined sound files from a designated directory.
    """
    def __init__(self):
        pygame.mixer.init()     # Initialize the pygame mixer

        # Directory where sound files are stored
        self.sounds_dir = "sounds"

        # Dictionary mapping sound names to filenames
        self.sounds = {
            "life_lost": "life_lost.wav",
            "bounce": "bounce.wav",
            "powerup": "powerup.wav",
            "powerdown": "powerdown.wav",
            "next_level": "next_level.wav",
            "hit_block": "hit_block.wav",
            "game_over": "game_over.wav"
        }

        # Dictionary to hold loaded pygame Sound objects
        self.loaded = {}

        # Load each sound file if it exists
        for name, filename in self.sounds.items():
            path = os.path.join(self.sounds_dir, filename)
            if os.path.exists(path):
                self.loaded[name] = pygame.mixer.Sound(path)
            else:
                print(f"[WARNING] Sound '{name}' not found at: {path}")

    def play(self, name):
        """
        Plays the sound associated with the given name if it's loaded.

        :param name: (str) The name of the sound to play.
        :return: None
        """
        if name in self.loaded:
            self.loaded[name].play()
        else:
            print(f"[ERROR] Sound '{name}' not loaded.")
