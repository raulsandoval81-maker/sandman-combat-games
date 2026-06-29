import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wrestling Two Player Game")

font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 54)
huge_font = pygame.font.SysFont(None, 76)
clock = pygame.time.Clock()

MATCH_SECONDS = 60
TECH_SCORE = 10
ATTACK_COOLDOWN_FRAMES = 45
CUTAWAY_FRAMES = 55

SPRITE_SIZE = (120, 160)
SCENE_SIZE = (460, 290)
SCENE_POS = (370, 260)

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

green_img = load_sprite("green_neutral_sprite.png")
red_img = load_sprite("red_neutral_sprite.png")

# Flip if needed. If it looks wrong, remove this or flip red instead.
if green_img:
    green_img = pygame.transform.flip(green_img, True, False)

scenes = {
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

mode = "menu"

green_x, green_y = 330, 380
red_x, red_y = 720, 380

green_score = 0
red_score = 0
green_actions = 0
red_actions = 0

green_cooldown = 0
red_cooldown = 0

green_sprawl_timer = 0
red_sprawl_timer = 0

cutaway_key = None
cutaway_timer = 0

start_ticks = pygame.time.get_ticks()
game_over = False
winner_text = ""
last_action_text = "Ready"
last_points_text = ""

def draw_text(text, x, y, color=(255, 255, 255), f=font):
    img = f.render(text, True, color)
    screen.blit(img, (x, y))

def start_cutaway(key, frames=CUTAWAY_FRAMES):
    global cutaway_key, cutaway_timer
    cutaway_key = key
    cutaway_timer = frames

def reset_game():
    global green_x, green_y, red_x, red_y
    global green_score, red_score, green_actions, red_actions
    global green_cooldown, red_cooldown
    global green_sprawl_timer, red_sprawl_timer
    global cutaway_key, cutaway_timer
    global start_ticks, game_over, winner_text
    global last_action_text, last_points_text, mode

    green_x, green_y = 330, 380
    red_x, red_y = 720, 380

    green_score = 0
    red_score = 0
    green_actions = 0
    red_actions = 0

    green_cooldown = 0
    red_cooldown = 0
    green_sprawl_timer = 0
    red_sprawl_timer = 0

    cutaway_key = None
    cutaway_timer = 0

    start_ticks = pygame.time.get_ticks()
    game_over = False
    winner_text = ""
    last_action_text = "Two-player match started"
    last_points_text = ""
    mode = "playing"

def distance():
    dx = green_x - red_x
    dy = green_y - red_y
    return (dx * dx + dy * dy) ** 0.5

def end_game(text):
    global game_over, winner_text
    game_over = True
    winner_text = text

running = True

while running:
    screen.fill((8, 8, 8))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if mode == "menu":
                if event.key == pygame.K_RETURN:
                    reset_game()

            elif not game_over:

                # GREEN PLAYER ATTACKS
                if event.key == pygame.K_SPACE and green_cooldown == 0:
                    if distance() < 210:
                        if red_sprawl_timer > 0:
                            green_cooldown = ATTACK_COOLDOWN_FRAMES
                            last_action_text = "Red sprawled Green shot!"
                            last_points_text = "No score"
                            start_cutaway("red_sprawl", 40)
                        else:
                            green_score += 2
                            green_actions += 1
                            green_cooldown = ATTACK_COOLDOWN_FRAMES
                            last_action_text = "Green double leg!"
                            last_points_text = "+2"
                            start_cutaway("green_takedown")
                    else:
                        last_action_text = "Green too far for takedown"
                        last_points_text = ""

                elif event.key == pygame.K_e and green_cooldown == 0:
                    if distance() < 180:
                        green_score += 4
                        green_actions += 1
                        green_cooldown = ATTACK_COOLDOWN_FRAMES + 20
                        last_action_text = "Green 4-point throw!"
                        last_points_text = "+4"
                        start_cutaway("green_4pt")

                elif event.key == pygame.K_f and green_cooldown == 0:
                    if distance() < 160:
                        green_score += 5
                        green_actions += 1
                        green_cooldown = ATTACK_COOLDOWN_FRAMES + 30
                        last_action_text = "Green suplex!"
                        last_points_text = "+5"
                        start_cutaway("green_5pt")

                elif event.key == pygame.K_g and green_cooldown == 0:
                    if distance() < 180:
                        green_score += 2
                        green_actions += 1
                        green_cooldown = ATTACK_COOLDOWN_FRAMES
                        last_action_text = "Green gut wrench!"
                        last_points_text = "+2"
                        start_cutaway("green_gut")

                elif event.key == pygame.K_LSHIFT:
                    green_actions += 1
                    green_sprawl_timer = 35
                    last_action_text = "Green sprawl defense"
                    last_points_text = "Defense active"
                    start_cutaway("green_sprawl", 35)

                # RED PLAYER ATTACKS
                elif event.key == pygame.K_RETURN and red_cooldown == 0:
                    if distance() < 210:
                        if green_sprawl_timer > 0:
                            red_cooldown = ATTACK_COOLDOWN_FRAMES
                            last_action_text = "Green sprawled Red shot!"
                            last_points_text = "No score"
                            start_cutaway("green_sprawl", 40)
                        else:
                            red_score += 2
                            red_actions += 1
                            red_cooldown = ATTACK_COOLDOWN_FRAMES
                            last_action_text = "Red double leg!"
                            last_points_text = "+2"
                            start_cutaway("red_takedown")
                    else:
                        last_action_text = "Red too far for takedown"
                        last_points_text = ""

                elif event.key == pygame.K_k and red_cooldown == 0:
                    if distance() < 180:
                        red_score += 4
                        red_actions += 1
                        red_cooldown = ATTACK_COOLDOWN_FRAMES + 20
                        last_action_text = "Red 4-point throw!"
                        last_points_text = "+4"
                        start_cutaway("red_4pt")

                elif event.key == pygame.K_l and red_cooldown == 0:
                    if distance() < 160:
                        red_score += 5
                        red_actions += 1
                        red_cooldown = ATTACK_COOLDOWN_FRAMES + 30
                        last_action_text = "Red suplex!"
                        last_points_text = "+5"
                        start_cutaway("red_5pt")

                elif event.key == pygame.K_SEMICOLON and red_cooldown == 0:
                    if distance() < 180:
                        red_score += 2
                        red_actions += 1
                        red_cooldown = ATTACK_COOLDOWN_FRAMES
                        last_action_text = "Red gut wrench!"
                        last_points_text = "+2"
                        start_cutaway("red_gut")

                elif event.key == pygame.K_RSHIFT:
                    red_actions += 1
                    red_sprawl_timer = 35
                    last_action_text = "Red sprawl defense"
                    last_points_text = "Defense active"
                    start_cutaway("red_sprawl", 35)

            elif game_over:
                if event.key == pygame.K_r:
                    mode = "menu"

    if mode == "menu":
        draw_text("WRESTLING TWO PLAYER", 300, 110, (255, 255, 255), huge_font)
        draw_text("Press ENTER to start", 410, 230, (255, 220, 50), big_font)
        draw_text("Green: WASD / SPACE / E / F / G / Left Shift", 275, 330, (40, 255, 80), font)
        draw_text("Red: Arrow Keys / ENTER / K / L / ; / Right Shift", 275, 375, (255, 70, 70), font)
        pygame.display.update()
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()

    seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, MATCH_SECONDS - seconds_passed)
    minutes = time_left // 60
    seconds = time_left % 60

    if not game_over:
        if green_cooldown > 0:
            green_cooldown -= 1
        if red_cooldown > 0:
            red_cooldown -= 1
        if green_sprawl_timer > 0:
            green_sprawl_timer -= 1
        if red_sprawl_timer > 0:
            red_sprawl_timer -= 1
        if cutaway_timer > 0:
            cutaway_timer -= 1
        else:
            cutaway_key = None

        # GREEN MOVEMENT
        if keys[pygame.K_a]:
            green_x -= 5
        if keys[pygame.K_d]:
            green_x += 5
        if keys[pygame.K_w]:
            green_y -= 5
        if keys[pygame.K_s]:
            green_y += 5

        # RED MOVEMENT
        if keys[pygame.K_LEFT]:
            red_x -= 5
        if keys[pygame.K_RIGHT]:
            red_x += 5
        if keys[pygame.K_UP]:
            red_y -= 5
        if keys[pygame.K_DOWN]:
            red_y += 5

        green_x = max(80, min(green_x, 1000))
        green_y = max(300, min(green_y, 470))
        red_x = max(80, min(red_x, 1000))
        red_y = max(300, min(red_y, 470))

        if green_score >= TECH_SCORE:
            end_game("GREEN WINS!")
        elif red_score >= TECH_SCORE:
            end_game("RED WINS!")
        elif time_left <= 0:
            if green_score > red_score:
                end_game("GREEN WINS BY DECISION!")
            elif red_score > green_score:
                end_game("RED WINS BY DECISION!")
            else:
                end_game("DRAW!")

    # HUD
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, 80))
    draw_text(f"Green: {green_score}", 25, 20, (40, 255, 80), big_font)
    draw_text(f"Red: {red_score}", 250, 20, (255, 70, 70), big_font)
    draw_text("Mode: TWO PLAYER", 520, 25, (255, 220, 50), font)
    draw_text(f"Time: {minutes}:{seconds:02d}", 930, 18, (255, 255, 255), big_font)

    # Gym wall
    pygame.draw.rect(screen, (38, 38, 38), (0, 80, WIDTH, 180))
    pygame.draw.rect(screen, (18, 32, 52), (0, 200, WIDTH, 80))
    draw_text("WRESTLING ROOM", 400, 125, (255, 200, 50), huge_font)

    # Mat
    pygame.draw.rect(screen, (18, 25, 45), (40, 255, 1120, 330))
    pygame.draw.circle(screen, (255, 215, 80), (600, 420), 245, 7)
    pygame.draw.circle(screen, (255, 255, 255), (600, 420), 250, 2)
    pygame.draw.circle(screen, (255, 215, 80), (600, 420), 78, 5)

    # Cutaway or live sprites
    if cutaway_key and scenes.get(cutaway_key):
        pygame.draw.rect(screen, (6, 10, 18), (355, 245, 490, 315), border_radius=14)
        pygame.draw.rect(screen, (255, 215, 80), (355, 245, 490, 315), 3, border_radius=14)
        screen.blit(scenes[cutaway_key], SCENE_POS)
        draw_text("ACTION CUTAWAY", 500, 250, (255, 220, 50), font)
    else:
        if green_img:
            screen.blit(green_img, (green_x, green_y))
        else:
            pygame.draw.circle(screen, (40, 255, 80), (int(green_x), int(green_y)), 35)

        if red_img:
            screen.blit(red_img, (red_x, red_y))
        else:
            pygame.draw.circle(screen, (255, 70, 70), (int(red_x), int(red_y)), 35)

    # Last action
    pygame.draw.rect(screen, (15, 15, 15), (25, 500, 250, 100), border_radius=10)
    draw_text("LAST ACTION", 55, 515, (255, 220, 50), font)
    draw_text(last_action_text, 45, 545, (255, 255, 255), font)
    draw_text(last_points_text, 90, 570, (40, 255, 80), font)

    # Controls
    pygame.draw.rect(screen, (18, 18, 18), (300, 590, 860, 55), border_radius=8)
    draw_text("GREEN: WASD SPACE E F G LSHIFT", 325, 602, (40, 255, 80), font)
    draw_text("RED: ARROWS ENTER K L ; RSHIFT", 325, 625, (255, 70, 70), font)

    draw_text(f"Green cooldown: {green_cooldown}", 35, 655, (40, 255, 80))
    draw_text(f"Red cooldown: {red_cooldown}", 260, 655, (255, 70, 70))
    draw_text("LOCAL TWO PLAYER: LIVE", 530, 655, (80, 180, 255))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        win_text = huge_font.render(winner_text, True, (255, 255, 255))
        restart_text = font.render("Press R to return to menu", True, (255, 255, 255))
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 280))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 360))

    pygame.display.update()
    clock.tick(60)

pygame.quit()