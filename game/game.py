import pygame


from game.console import CONSOLE_OPTIONS, get_default_console
from game.settings import WIDTH, HEIGHT
from game.player import create_players
from game.animation import AnimationManager
from game.timer import MatchTimer
from game.ui import UI
from game.controls import handle_action_input, handle_keydown, handle_movement
from game.mobile_input import MobileInput
from game.scoring import check_tech_fall, decision_winner
from game.grapple import GrappleState


class WrestlingGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption("Wrestling Two Player Game")



        self.console_options = CONSOLE_OPTIONS
        self.selected_console = 0
        self.console_style = get_default_console()
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)
        self.mobile_input = MobileInput()
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
        self.mobile_input.reset()
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
                elif event.button == 1 and not getattr(event, "touch", False):
                    self.mobile_input.pointer_down(
                        "mouse", event.pos, self.handle_mobile_action
                    )

            elif event.type == pygame.MOUSEMOTION:
                if not getattr(event, "touch", False):
                    self.mobile_input.pointer_motion("mouse", event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and not getattr(event, "touch", False):
                    self.mobile_input.pointer_up("mouse")

            elif event.type == pygame.FINGERDOWN:
                if self.mode == "menu":
                    self.reset_game()
                else:
                    self.mobile_input.pointer_down(
                        event.finger_id,
                        self.finger_position(event),
                        self.handle_mobile_action,
                    )

            elif event.type == pygame.FINGERMOTION:
                self.mobile_input.pointer_motion(
                    event.finger_id, self.finger_position(event)
                )

            elif event.type == pygame.FINGERUP:
                self.mobile_input.pointer_up(event.finger_id)

    def finger_position(self, event):
        width, height = self.screen.get_size()
        return event.x * width, event.y * height

    def handle_mobile_action(self, action):
        handle_action_input(
            action,
            self,
            player="green",
            direction=self.mobile_input.joystick_vector,
            active_actions=self.mobile_input.pressed_actions,
        )

    def update(self):
        if self.mode == "menu" or self.game_over:
            return

        if self.animation.cutaway_timer <= 0:
            keys = pygame.key.get_pressed()
            handle_movement(
                keys,
                self.green,
                self.red,
                self.grapple,
                self.mobile_input.joystick_vector,
            )

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
