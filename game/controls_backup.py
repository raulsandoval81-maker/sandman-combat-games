import pygame
from game.settings import (
    ATTACK_COOLDOWN_FRAMES,
    PLAYER_MIN_X, PLAYER_MAX_X,
    PLAYER_MIN_Y, PLAYER_MAX_Y,
    PLAYER_SPEED,
)
from game.collision import in_range
from game.scoring import award_points


def clamp_players(green, red):
    green.x = max(PLAYER_MIN_X, min(green.x, PLAYER_MAX_X))
    green.y = max(PLAYER_MIN_Y, min(green.y, PLAYER_MAX_Y))
    red.x = max(PLAYER_MIN_X, min(red.x, PLAYER_MAX_X))
    red.y = max(PLAYER_MIN_Y, min(red.y, PLAYER_MAX_Y))


def handle_movement(keys, green, red, grapple=None):
    speed = PLAYER_SPEED

    if grapple and grapple.movement_speed():
        speed = grapple.movement_speed()

    if keys[pygame.K_a]:
        green.x -= speed
    if keys[pygame.K_d]:
        green.x += speed
    if keys[pygame.K_w]:
        green.y -= speed
    if keys[pygame.K_s]:
        green.y += speed

    if keys[pygame.K_LEFT]:
        red.x -= speed
    if keys[pygame.K_RIGHT]:
        red.x += speed
    if keys[pygame.K_UP]:
        red.y -= speed
    if keys[pygame.K_DOWN]:
        red.y += speed

    clamp_players(green, red)


def handle_keydown(event, game):
    green = game.green
    red = game.red
    animation = game.animation

    if game.mode == "menu":
        if event.key == pygame.K_RETURN:
            game.reset_game()
        return

    if game.game_over:
        if event.key == pygame.K_r:
            game.mode = "menu"
        return

    # GRAPPLING CONTROLS
    if event.key == pygame.K_c:
        game.grapple.enter_collar_tie("green")
        game.last_action_text = game.grapple.message
        game.last_points_text = "Control"
        return

    if event.key == pygame.K_m:
        game.grapple.enter_collar_tie("red")
        game.last_action_text = game.grapple.message
        game.last_points_text = "Control"
        return

    if event.key == pygame.K_b:
        game.grapple.break_grapple()
        game.last_action_text = game.grapple.message
        game.last_points_text = ""
        return

    # GREEN ATTACKS
    if event.key == pygame.K_SPACE and green.cooldown == 0:
        if game.grapple.state != "COLLAR_TIE":
            game.last_action_text = "Green needs a tie-up first"
            game.last_points_text = ""
            return

        if game.grapple.control != "green":
            game.last_action_text = "Green needs control first"
            game.last_points_text = ""
            return

        if in_range(green, red, 210):
            if red.sprawl_timer > 0:
                green.cooldown = ATTACK_COOLDOWN_FRAMES
                game.last_action_text = "Red sprawled Green shot!"
                game.last_points_text = "No score"
                animation.start_cutaway("red_sprawl", 40)
            else:
                award_points(green, 2)
                green.cooldown = ATTACK_COOLDOWN_FRAMES
                game.last_action_text = "Green double leg from collar tie!"
                game.last_points_text = "+2"
                animation.start_cutaway("green_takedown")
        return

    elif event.key == pygame.K_e and green.cooldown == 0:
        if in_range(green, red, 180):
            award_points(green, 4)
            green.cooldown = ATTACK_COOLDOWN_FRAMES + 20
            game.last_action_text = "Green 4-point throw!"
            game.last_points_text = "+4"
            animation.start_cutaway("green_4pt")
        return

    elif event.key == pygame.K_f and green.cooldown == 0:
        if in_range(green, red, 160):
            award_points(green, 5)
            green.cooldown = ATTACK_COOLDOWN_FRAMES + 30
            game.last_action_text = "Green suplex!"
            game.last_points_text = "+5"
            animation.start_cutaway("green_5pt")
        return

    elif event.key == pygame.K_g and green.cooldown == 0:
        if in_range(green, red, 180):
            award_points(green, 2)
            green.cooldown = ATTACK_COOLDOWN_FRAMES
            game.last_action_text = "Green gut wrench!"
            game.last_points_text = "+2"
            animation.start_cutaway("green_gut")
        return

    elif event.key == pygame.K_LSHIFT:
        green.actions += 1
        green.sprawl_timer = 35
        game.last_action_text = "Green sprawl defense"
        game.last_points_text = "Defense active"
        animation.start_cutaway("green_sprawl", 35)
        return

    # RED ATTACKS
    elif event.key == pygame.K_RETURN and red.cooldown == 0:
        if game.grapple.state != "COLLAR_TIE":
            game.last_action_text = "Red needs a tie-up first"
            game.last_points_text = ""
            return

        if game.grapple.control != "red":
            game.last_action_text = "Red needs control first"
            game.last_points_text = ""
            return

        if in_range(red, green, 210):
            if green.sprawl_timer > 0:
                red.cooldown = ATTACK_COOLDOWN_FRAMES
                game.last_action_text = "Green sprawled Red shot!"
                game.last_points_text = "No score"
                animation.start_cutaway("green_sprawl", 40)
            else:
                award_points(red, 2)
                red.cooldown = ATTACK_COOLDOWN_FRAMES
                game.last_action_text = "Red double leg from collar tie!"
                game.last_points_text = "+2"
                animation.start_cutaway("red_takedown")
        return

    elif event.key == pygame.K_k and red.cooldown == 0:
        if in_range(red, green, 180):
            award_points(red, 4)
            red.cooldown = ATTACK_COOLDOWN_FRAMES + 20
            game.last_action_text = "Red 4-point throw!"
            game.last_points_text = "+4"
            animation.start_cutaway("red_4pt")
        return

    elif event.key == pygame.K_l and red.cooldown == 0:
        if in_range(red, green, 160):
            award_points(red, 5)
            red.cooldown = ATTACK_COOLDOWN_FRAMES + 30
            game.last_action_text = "Red suplex!"
            game.last_points_text = "+5"
            animation.start_cutaway("red_5pt")
        return

    elif event.key == pygame.K_SEMICOLON and red.cooldown == 0:
        if in_range(red, green, 180):
            award_points(red, 2)
            red.cooldown = ATTACK_COOLDOWN_FRAMES
            game.last_action_text = "Red gut wrench!"
            game.last_points_text = "+2"
            animation.start_cutaway("red_gut")
        return

    elif event.key == pygame.K_RSHIFT:
        red.actions += 1
        red.sprawl_timer = 35
        game.last_action_text = "Red sprawl defense"
        game.last_points_text = "Defense active"
        animation.start_cutaway("red_sprawl", 35)
        return