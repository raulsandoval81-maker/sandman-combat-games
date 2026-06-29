import pygame
from game.settings import MATCH_SECONDS

class MatchTimer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.start_ticks = pygame.time.get_ticks()

    def time_left(self):
        seconds_passed = (pygame.time.get_ticks() - self.start_ticks) // 1000
        return max(0, MATCH_SECONDS - seconds_passed)

    def formatted(self):
        left = self.time_left()
        minutes = left // 60
        seconds = left % 60
        return minutes, seconds

    def is_finished(self):
        return self.time_left() <= 0
