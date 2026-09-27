import pygame
from game.settings import WIDTH, HEIGHT, SCENE_POS


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 24)
        self.big_font = pygame.font.SysFont(None, 54)
        self.huge_font = pygame.font.SysFont(None, 76)

    def draw_text(self, text, x, y, color=(255, 255, 255), font=None):
        if font is None:
            font = self.font
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def draw_splash_background(self):
        self.screen.fill((5, 6, 12))

        points = [(520, 0), (680, 0), (860, 650), (340, 650)]
        spotlight = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(spotlight, (255, 240, 180, 45), points)
        self.screen.blit(spotlight, (0, 0))

        pygame.draw.ellipse(self.screen, (18, 25, 45), (250, 390, 700, 190))
        pygame.draw.ellipse(self.screen, (255, 215, 80), (270, 405, 660, 160), 5)
        pygame.draw.ellipse(self.screen, (255, 255, 255), (330, 425, 540, 120), 2)
        pygame.draw.ellipse(self.screen, (255, 215, 80), (520, 450, 160, 55), 4)

    def draw_menu(self):
        self.draw_splash_background()
        self.draw_text("SANDMAN COMBAT GAMES", 255, 70, (255, 255, 255), self.huge_font)
        self.draw_text("> Quick Match", 455, 185, (255, 220, 50), self.big_font)
        self.draw_text("  Career Mode", 455, 240, (220, 220, 220), self.big_font)
        self.draw_text("  Training Arena", 455, 295, (220, 220, 220), self.big_font)
        self.draw_text("  Settings", 455, 350, (220, 220, 220), self.big_font)
        self.draw_text("Tap / Click / Press ENTER", 425, 610, (255, 220, 50), self.font)

    def draw_stamina_bars(self, game):
        green_stamina = 0.82
        red_stamina = 0.76

        pygame.draw.rect(self.screen, (20, 20, 25), (25, 60, 300, 10), border_radius=5)
        pygame.draw.rect(self.screen, (40, 255, 80), (25, 60, int(300 * green_stamina), 10), border_radius=5)

        pygame.draw.rect(self.screen, (20, 20, 25), (875, 60, 300, 10), border_radius=5)
        pygame.draw.rect(self.screen, (255, 70, 70), (875, 60, int(300 * red_stamina), 10), border_radius=5)

    def draw_state_chip(self, game):
        labels = {
            "NEUTRAL": "NEUTRAL",
            "CONTACT": "HAND FIGHT",
            "COLLAR_TIE": "COLLAR TIE",
            "TOP_BOTTOM": "MAT CONTROL",
        }
        label = labels.get(game.grapple.state, game.grapple.state.replace("_", " "))
        text = self.small_font.render(label, True, (255, 225, 110))
        width = text.get_width() + 28
        x = WIDTH // 2 - width // 2
        pygame.draw.rect(self.screen, (18, 20, 28), (x, 86, width, 30), border_radius=15)
        pygame.draw.rect(self.screen, (105, 90, 45), (x, 86, width, 30), 1, border_radius=15)
        self.screen.blit(text, (x + 14, 92))

    def draw_mobile_overlay(self, mobile_input):
        joystick_x, joystick_y = mobile_input.JOYSTICK_CENTER
        knob_x, knob_y = mobile_input.joystick_knob_position

        pygame.draw.circle(self.screen, (8, 8, 12), (joystick_x, joystick_y), 58)
        pygame.draw.circle(self.screen, (35, 35, 45), (joystick_x, joystick_y), 52)
        pygame.draw.circle(self.screen, (255, 220, 50), (joystick_x, joystick_y), 52, 2)
        pygame.draw.circle(self.screen, (95, 95, 115), (knob_x, knob_y), 23)
        pygame.draw.circle(self.screen, (180, 180, 200), (knob_x, knob_y), 23, 2)

        buttons = [
            ("triangle", "△", (60, 220, 120)),
            ("circle", "○", (255, 80, 80)),
            ("square", "□", (255, 120, 200)),
            ("cross", "×", (80, 160, 255)),
        ]

        for action, label, color in buttons:
            x, y = mobile_input.button_centers[action]
            pressed = action in mobile_input.pressed_actions
            pygame.draw.circle(self.screen, (8, 8, 12), (x, y), 32)
            fill = color if pressed else (35, 35, 45)
            pygame.draw.circle(self.screen, fill, (x, y), 28)
            pygame.draw.circle(self.screen, color, (x, y), 28, 3)
            text_color = (8, 8, 12) if pressed else color
            text = self.big_font.render(label, True, text_color)
            self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    def draw_wrestler(self, image, x, y, color):
        px = int(x)
        py = int(y)
        pygame.draw.ellipse(self.screen, (4, 5, 8), (px - 44, py + 28, 88, 24))
        if image:
            self.screen.blit(image, (px, py))
        else:
            pygame.draw.circle(self.screen, color, (px, py), 35)
            pygame.draw.circle(self.screen, (245, 245, 245), (px, py), 35, 2)

    def draw_game(self, game):
        green = game.green
        red = game.red
        animation = game.animation
        minutes, seconds = game.timer.formatted()

        self.screen.fill((6, 8, 13))

        # Broadcast-style scoreboard: information first, decoration second.
        pygame.draw.rect(self.screen, (4, 5, 8), (0, 0, WIDTH, 82))
        pygame.draw.line(self.screen, (45, 48, 58), (0, 81), (WIDTH, 81), 1)
        self.draw_text(f"GREEN  {green.score}", 25, 16, (40, 255, 80), self.big_font)

        timer_text = self.big_font.render(f"{minutes}:{seconds:02d}", True, (255, 255, 255))
        self.screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 16))

        red_text = self.big_font.render(f"{red.score}  RED", True, (255, 70, 70))
        self.screen.blit(red_text, (WIDTH - red_text.get_width() - 25, 16))
        self.draw_stamina_bars(game)
        self.draw_state_chip(game)

        # Arena depth layers.
        pygame.draw.rect(self.screen, (20, 23, 31), (0, 82, WIDTH, 145))
        pygame.draw.rect(self.screen, (11, 17, 27), (0, 190, WIDTH, 92))
        pygame.draw.line(self.screen, (55, 58, 68), (0, 226), (WIDTH, 226), 1)

        mat_rect = pygame.Rect(40, 238, 1120, 362)
        pygame.draw.rect(self.screen, (14, 22, 38), mat_rect, border_radius=24)
        pygame.draw.rect(self.screen, (30, 38, 58), mat_rect, 2, border_radius=24)
        pygame.draw.circle(self.screen, (255, 215, 80), (600, 420), 245, 6)
        pygame.draw.circle(self.screen, (220, 225, 235), (600, 420), 250, 2)
        pygame.draw.circle(self.screen, (255, 215, 80), (600, 420), 78, 4)

        if animation.cutaway_key and animation.scenes.get(animation.cutaway_key):
            pygame.draw.rect(self.screen, (6, 10, 18), (355, 245, 490, 315), border_radius=14)
            pygame.draw.rect(self.screen, (255, 215, 80), (355, 245, 490, 315), 3, border_radius=14)
            self.screen.blit(animation.scenes[animation.cutaway_key], SCENE_POS)
            self.draw_text("ACTION", 555, 250, (255, 220, 50), self.font)
        else:
            self.draw_wrestler(animation.green_img, green.x, green.y, (40, 255, 80))
            self.draw_wrestler(animation.red_img, red.x, red.y, (255, 70, 70))

        # Compact action feed instead of a large debug-looking box.
        pygame.draw.rect(self.screen, (8, 10, 15), (330, 610, 540, 66), border_radius=16)
        self.draw_text(game.last_action_text, 360, 621, (240, 242, 248), self.small_font)
        if game.last_points_text:
            self.draw_text(game.last_points_text, 360, 646, (255, 220, 70), self.small_font)

        self.draw_mobile_overlay(game.mobile_input)

        if game.game_over:
            self.draw_game_over(game.winner_text)

    def draw_game_over(self, winner_text):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(215)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        self.draw_text("MATCH COMPLETE", 430, 225, (255, 220, 70), self.big_font)
        win_text = self.huge_font.render(winner_text, True, (255, 255, 255))
        restart_text = self.font.render("Press R to return to menu", True, (210, 214, 224))
        self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 290))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 380))
