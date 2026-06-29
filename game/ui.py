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

    def draw_menu(self):
        self.screen.fill((8, 8, 8))
        self.draw_text("WRESTLING TWO PLAYER", 300, 110, (255, 255, 255), self.huge_font)
        self.draw_text("Press ENTER to start", 410, 230, (255, 220, 50), self.big_font)
        self.draw_text("Green: WASD / C tie / SPACE shot / G turn / LSHIFT sprawl", 230, 330, (40, 255, 80), self.font)
        self.draw_text("Red: Arrows / M tie / ENTER shot / ; turn / RSHIFT sprawl", 230, 375, (255, 70, 70), self.font)

    def draw_game(self, game):
        green = game.green
        red = game.red
        animation = game.animation
        minutes, seconds = game.timer.formatted()

        self.screen.fill((8, 8, 8))

        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, WIDTH, 80))
        self.draw_text(f"Green: {green.score}", 25, 20, (40, 255, 80), self.big_font)
        self.draw_text(f"Red: {red.score}", 250, 20, (255, 70, 70), self.big_font)

        self.draw_text(f"Grapple: {game.grapple.state}", 500, 15, (80, 180, 255), self.font)
        self.draw_text(f"Top: {game.grapple.top_wrestler}", 500, 42, (255, 220, 50), self.font)

        turn_seconds = game.grapple.turn_timer // 60
        self.draw_text(f"Turn Window: {turn_seconds}", 700, 42, (255, 220, 50), self.font)

        self.draw_text(f"Time: {minutes}:{seconds:02d}", 930, 18, (255, 255, 255), self.big_font)

        pygame.draw.rect(self.screen, (38, 38, 38), (0, 80, WIDTH, 180))
        pygame.draw.rect(self.screen, (18, 32, 52), (0, 200, WIDTH, 80))
        self.draw_text("WRESTLING ROOM", 400, 125, (255, 200, 50), self.huge_font)

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

        pygame.draw.rect(self.screen, (18, 18, 18), (300, 590, 860, 55), border_radius=8)
        self.draw_text("GREEN: WASD / C Tie / SPACE Shot / G Turn / LSHIFT Sprawl", 325, 602, (40, 255, 80), self.font)
        self.draw_text("RED: Arrows / M Tie / ENTER Shot / ; Turn / RSHIFT Sprawl", 325, 625, (255, 70, 70), self.font)

        self.draw_text(f"Green cooldown: {green.cooldown}", 35, 655, (40, 255, 80))
        self.draw_text(f"Red cooldown: {red.cooldown}", 260, 655, (255, 70, 70))
        self.draw_text("LOCAL TWO PLAYER: LIVE", 530, 655, (80, 180, 255))

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
