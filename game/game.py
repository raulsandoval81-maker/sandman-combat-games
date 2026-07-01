import pygame

from game.settings import WIDTH, HEIGHT
from game.player import create_players
from game.animation import AnimationManager
from game.timer import MatchTimer
from game.ui import UI
from game.controls import handle_keydown, handle_movement
from game.scoring import check_tech_fall, decision_winner
from game.grapple import GrappleState


class WrestlingGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Wrestling Two Player Game")

        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)
        self.animation = AnimationManager()
        self.timer = MatchTimer()
        self.grapple = GrappleState()
        self.green, self.red = create_players()

        self.mode = "menu"
        self.running = True
        self.game_over = False
        self.winner_text = ""
        self.last_action_text = "Ready"
        self.last_points_text = ""

    def reset_game(self):
        self.green.reset()
        self.red.reset()
        self.animation.reset()
        self.timer.reset()
        self.grapple.reset()
        self.game_over = False
        self.winner_text = ""
        self.last_action_text = "Two-player match started"
        self.last_points_text = ""
        self.mode = "playing"

    def end_game(self, text):
        self.game_over = True
        self.winner_text = text

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                handle_keydown(event, self)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.mode == "menu":
                    self.reset_game()

            elif event.type == pygame.FINGERDOWN:
                if self.mode == "menu":
                    self.reset_game()

    def update(self):
        if self.mode == "menu" or self.game_over:
            return

        keys = pygame.key.get_pressed()
        handle_movement(keys, self.green, self.red, self.grapple)

        self.green.tick()
        self.red.tick()
        self.animation.tick()
        self.grapple.update(self.green, self.red)
        self.grapple.tick_turn_timer()

        tech_result = check_tech_fall(self.green, self.red)
        if tech_result:
            self.end_game(tech_result)
        elif self.timer.is_finished():
            self.end_game(decision_winner(self.green, self.red))

    def draw(self):
        if self.mode == "menu":
            self.ui.draw_menu()
        else:
            self.ui.draw_game(self)
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    WrestlingGame().run()