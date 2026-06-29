import os
import pygame
from game.settings import SPRITE_SIZE, SCENE_SIZE, CUTAWAY_FRAMES

def load_sprite(filename, size=SPRITE_SIZE):
    path = os.path.join("assets", "sprites", filename)
    if not os.path.exists(path):
        print("Missing:", path)
        return None
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, size)

def load_scene(filename, size=SCENE_SIZE):
    path = os.path.join("assets", "scenes", filename)
    if not os.path.exists(path):
        print("Missing:", path)
        return None
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, size)

class AnimationManager:
    def __init__(self):
        self.green_img = load_sprite("green_neutral_sprite.png")
        self.red_img = load_sprite("red_neutral_sprite.png")

        if self.green_img:
            self.green_img = pygame.transform.flip(self.green_img, True, False)

        self.scenes = {
            "green_takedown": load_scene("greentakedown.png"),
            "red_takedown": load_scene("redtakedown.png"),
            "green_sprawl": load_scene("greensprawl.png"),
            "red_sprawl": load_scene("redsprawl.png"),
            "green_4pt": load_scene("green4ptmove.png"),
            "red_4pt": load_scene("red4ptmove.png"),
            "green_5pt": load_scene("green5ptmove.png"),
            "red_5pt": load_scene("red5ptmovered.png"),
            "green_gut": load_scene("greengutwrench.png"),
            "red_gut": load_scene("redgutwrench.png"),
        }

        self.cutaway_key = None
        self.cutaway_timer = 0

    def start_cutaway(self, key, frames=CUTAWAY_FRAMES):
        self.cutaway_key = key
        self.cutaway_timer = frames

    def reset(self):
        self.cutaway_key = None
        self.cutaway_timer = 0

    def tick(self):
        if self.cutaway_timer > 0:
            self.cutaway_timer -= 1
        else:
            self.cutaway_key = None
