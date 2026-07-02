import pygame
from game.settings import WIDTH, HEIGHT, SCENE_POS


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)
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

        pygame.draw.rect(self.screen, (20, 20, 25), (25, 55, 300, 14), border_radius=6)
        pygame.draw.rect(self.screen, (40, 255, 80), (25, 55, int(300 * green_stamina), 14), border_radius=6)

        pygame.draw.rect(self.screen, (20, 20, 25), (875, 55, 300, 14), border_radius=6)
        pygame.draw.rect(self.screen, (255, 70, 70), (875, 55, int(300 * red_stamina), 14), border_radius=6)

    def draw_mobile_overlay(self):
        pygame.draw.circle(self.screen, (8, 8, 12), (115, 575), 68)
        pygame.draw.circle(self.screen, (35, 35, 45), (115, 575), 60)
        pygame.draw.circle(self.screen, (255, 220, 50), (115, 575), 60, 2)
        pygame.draw.circle(self.screen, (95, 95, 115), (115, 575), 26)
        pygame.draw.circle(self.screen, (180, 180, 200), (115, 575), 26, 2)

        buttons = [
            ("△", 995, 550, (60, 220, 120)),
            ("○", 1085, 585, (255, 80, 80)),
            ("□", 905, 585, (255, 120, 200)),
            ("×", 995, 635, (80, 160, 255)),
        ]

        for label, x, y, color in buttons:
            pygame.draw.circle(self.screen, (8, 8, 12), (x, y), 42)
            pygame.draw.circle(self.screen, (35, 35, 45), (x, y), 36)
            pygame.draw.circle(self.screen, color, (x, y), 36, 3)
            text = self.big_font.render(label, True, color)
            self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    def draw_game(self, game):
        green = game.green
        red = game.red
        animation = game.animation
        minutes, seconds = game.timer.formatted()

        self.screen.fill((8, 8, 8))

        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, WIDTH, 80))
        self.draw_text(f"GREEN {green.score}", 25, 18, (40, 255, 80), self.big_font)

        timer_text = self.big_font.render(f"{minutes}:{seconds:02d}", True, (255, 255, 255))
        self.screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 18))

        red_text = self.big_font.render(f"{red.score} RED", True, (255, 70, 70))
        self.screen.blit(red_text, (WIDTH - red_text.get_width() - 25, 18))
        self.draw_stamina_bars(game)

        pygame.draw.rect(self.screen, (38, 38, 38), (0, 80, WIDTH, 180))
        pygame.draw.rect(self.screen, (18, 32, 52), (0, 200, WIDTH, 80))
        self.draw_text("ARENA MODE", 400, 125, (255, 200, 50), self.huge_font)

        pygame.draw.rect(self.screen, (18, 25, 45), (40, 255, 1120, 330))
        pygame.draw.circle(self.screen, (255, 215, 80), (600, 420), 245, 7)
        pygame.draw.circle(self.screen, (255, 255, 255), (600, 420), 250, 2)
        pygame.draw.circle(self.screen, (255, 215, 80), (600, 420), 78, 5)

        if animation.cutaway_key and animation.scenes.get(animation.cutaway_key):
            pygame.draw.rect(self.screen, (6, 10, 18), (355, 245, 490, 315), border_radius=14)
            pygame.draw.rect(self.screen, (255, 215, 80), (355, 245, 490, 315), 3, border_radius=14)
            self.screen.blit(animation.scenes[animation.cutaway_key], SCENE_POS)
            self.draw_text("ACTION CUTAWAY", 500, 250, (255, 220, 50), self.font)
        else:
            if animation.green_img:
                self.screen.blit(animation.green_img, (green.x, green.y))
            else:
                pygame.draw.circle(self.screen, (40, 255, 80), (int(green.x), int(green.y)), 35)

            if animation.red_img:
                self.screen.blit(animation.red_img, (red.x, red.y))
            else:
                pygame.draw.circle(self.screen, (255, 70, 70), (int(red.x), int(red.y)), 35)

        pygame.draw.rect(self.screen, (15, 15, 15), (25, 500, 250, 100), border_radius=10)
        self.draw_text("LAST ACTION", 55, 515, (255, 220, 50), self.font)
        self.draw_text(game.last_action_text, 45, 545, (255, 255, 255), self.font)
        self.draw_text(game.last_points_text, 90, 570, (40, 255, 80), self.font)

        self.draw_mobile_overlay()

        if game.game_over:
            self.draw_game_over(game.winner_text)

    def draw_game_over(self, winner_text):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        win_text = self.huge_font.render(winner_text, True, (255, 255, 255))
        restart_text = self.font.render("Press R to return to menu", True, (255, 255, 255))
        self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 280))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 360))
