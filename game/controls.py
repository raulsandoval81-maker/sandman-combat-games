import pygame
from game.settings import (
    ATTACK_COOLDOWN_FRAMES,
    PLAYER_MIN_X, PLAYER_MAX_X,
    PLAYER_MIN_Y, PLAYER_MAX_Y,
    PLAYER_SPEED,
)
from game.collision import in_range
from game.scoring import award_points


ACTION_NAMES = ("triangle", "circle", "square", "cross")
JOYSTICK_DEADZONE = 0.15


def clamp_players(green, red):
    green.x = max(PLAYER_MIN_X, min(green.x, PLAYER_MAX_X))
    green.y = max(PLAYER_MIN_Y, min(green.y, PLAYER_MAX_Y))
    red.x = max(PLAYER_MIN_X, min(red.x, PLAYER_MAX_X))
    red.y = max(PLAYER_MIN_Y, min(red.y, PLAYER_MAX_Y))

    if green.x in (PLAYER_MIN_X, PLAYER_MAX_X):
        green.vx = 0.0
    if green.y in (PLAYER_MIN_Y, PLAYER_MAX_Y):
        green.vy = 0.0
    if red.x in (PLAYER_MIN_X, PLAYER_MAX_X):
        red.vx = 0.0
    if red.y in (PLAYER_MIN_Y, PLAYER_MAX_Y):
        red.vy = 0.0


def _keyboard_axis(negative_pressed, positive_pressed):
    return float(bool(positive_pressed)) - float(bool(negative_pressed))


def _merge_axis(keyboard_value, analog_value):
    if abs(analog_value) > JOYSTICK_DEADZONE:
        return max(-1.0, min(1.0, analog_value))
    return keyboard_value


def handle_movement(keys, green, red, grapple=None, green_direction=(0.0, 0.0)):
    speed = PLAYER_SPEED

    if grapple:
        grapple_speed = grapple.movement_speed()
        if grapple_speed is not None:
            speed = grapple_speed

    analog_x, analog_y = green_direction
    green_dx = _merge_axis(
        _keyboard_axis(keys[pygame.K_a], keys[pygame.K_d]),
        analog_x,
    )
    green_dy = _merge_axis(
        _keyboard_axis(keys[pygame.K_w], keys[pygame.K_s]),
        analog_y,
    )

    red_dx = _keyboard_axis(keys[pygame.K_LEFT], keys[pygame.K_RIGHT])
    red_dy = _keyboard_axis(keys[pygame.K_UP], keys[pygame.K_DOWN])

    green.set_move_intent(green_dx, green_dy, speed)
    red.set_move_intent(red_dx, red_dy, speed)
    clamp_players(green, red)


def handle_action_input(
    action, game, player="green", direction=(0.0, 0.0), active_actions=frozenset()
):
    if action not in ACTION_NAMES:
        return False

    if player == "green":
        key_map = {
            "triangle": (
                pygame.K_g
                if game.grapple.state == "TOP_BOTTOM"
                and game.grapple.top_wrestler == "green"
                else pygame.K_c
            ),
            "circle": pygame.K_LSHIFT,
            "square": pygame.K_SPACE,
            "cross": pygame.K_e,
        }
    elif player == "red":
        key_map = {
            "triangle": (
                pygame.K_SEMICOLON
                if game.grapple.state == "TOP_BOTTOM"
                and game.grapple.top_wrestler == "red"
                else pygame.K_m
            ),
            "circle": pygame.K_RSHIFT,
            "square": pygame.K_RETURN,
            "cross": pygame.K_k,
        }
    else:
        return False

    handle_keydown(pygame.event.Event(pygame.KEYDOWN, key=key_map[action]), game)
    return True


def _start_shot(game, attacker_name, attacker, defender, animation_key):
    if attacker.cooldown > 0:
        return

    if not in_range(attacker, defender, 210):
        game.last_action_text = f"{attacker_name.title()} is too far away to shoot"
        game.last_points_text = "Close distance first"
        return

    if not game.grapple.start_shot(attacker_name):
        game.last_action_text = "Win contact or tie control before shooting"
        game.last_points_text = "Hand fight first"
        return

    attacker.cooldown = ATTACK_COOLDOWN_FRAMES
    attacker.actions += 1
    attacker.stop_motion()
    defender.stop_motion()
    game.last_action_text = f"{attacker_name.title()} attacks the legs!"
    game.last_points_text = "DEFEND NOW · sprawl window"


def _attempt_sprawl(game, wrestler_name, wrestler):
    if game.grapple.state != "SCRAMBLE":
        if game.grapple.state not in ("CONTACT", "COLLAR_TIE"):
            game.last_action_text = f"{wrestler_name.title()} must be engaged to defend"
            game.last_points_text = ""
        else:
            game.last_action_text = "No active shot to defend"
            game.last_points_text = "Stay ready"
        return

    if not game.grapple.attempt_sprawl(wrestler_name):
        game.last_action_text = f"{wrestler_name.title()} is attacking — cannot sprawl own shot"
        game.last_points_text = ""
        return

    wrestler.actions += 1
    wrestler.sprawl_timer = 35
    game.last_action_text = f"{wrestler_name.title()} sprawls on the shot!"
    game.last_points_text = "SCRAMBLE · hold position"


def _hand_fight(game, wrestler_name):
    if not game.grapple.hand_fight(wrestler_name):
        game.last_action_text = f"{wrestler_name.title()} needs contact to hand fight"
        game.last_points_text = "Close distance"
        return

    progress, threshold = game.grapple.control_progress(wrestler_name)
    game.last_action_text = game.grapple.message
    if game.grapple.control == wrestler_name and progress >= threshold:
        game.last_points_text = "INSIDE CONTROL WON · attacks opened"
    else:
        game.last_points_text = f"HAND FIGHT · {progress}/{threshold} pressure"


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

    # A finished-action cutaway locks new attacks. The live SCRAMBLE state does
    # not start a cutaway, so the defender can still react with a sprawl.
    if animation.cutaway_timer > 0:
        return

    # HAND FIGHT / TIE CONTROL
    if event.key == pygame.K_c:
        _hand_fight(game, "green")
        return

    if event.key == pygame.K_m:
        _hand_fight(game, "red")
        return

    if event.key == pygame.K_b:
        game.grapple.break_grapple()
        game.last_action_text = game.grapple.message
        game.last_points_text = ""
        return

    # TOP CONTROL / TURN
    if event.key == pygame.K_g:
        if game.grapple.can_turn("green"):
            game.grapple.record_turn("green")
            award_points(green, 2)
            game.last_action_text = "Green turns Red!"
            game.last_points_text = "+2 near fall"
            animation.start_cutaway("green_gut")
        else:
            game.last_action_text = "Green needs top position to turn"
            game.last_points_text = ""
        return

    if event.key == pygame.K_SEMICOLON:
        if game.grapple.can_turn("red"):
            game.grapple.record_turn("red")
            award_points(red, 2)
            game.last_action_text = "Red turns Green!"
            game.last_points_text = "+2 near fall"
            animation.start_cutaway("red_gut")
        else:
            game.last_action_text = "Red needs top position to turn"
            game.last_points_text = ""
        return

    # SHOTS: contact is enough; tie control blocks the opponent's clean entry.
    if event.key == pygame.K_SPACE:
        _start_shot(game, "green", green, red, "green_takedown")
        return

    if event.key == pygame.K_RETURN:
        _start_shot(game, "red", red, green, "red_takedown")
        return

    # LIVE DEFENSE DURING SHOT WINDOW
    if event.key == pygame.K_LSHIFT:
        _attempt_sprawl(game, "green", green)
        return

    if event.key == pygame.K_RSHIFT:
        _attempt_sprawl(game, "red", red)
        return

    # BIG MOVES remain tie-control attacks for now.
    if event.key == pygame.K_e and green.cooldown == 0:
        if (
            game.grapple.state == "COLLAR_TIE"
            and game.grapple.control == "green"
            and in_range(green, red, 180)
        ):
            award_points(green, 4)
            green.cooldown = ATTACK_COOLDOWN_FRAMES + 20
            game.last_action_text = "Green 4-point throw!"
            game.last_points_text = "+4"
            animation.start_cutaway("green_4pt")
            game.grapple.start_top_bottom("green")
        else:
            game.last_action_text = "Green needs tie control for the throw"
            game.last_points_text = ""
        return

    if event.key == pygame.K_f and green.cooldown == 0:
        if (
            game.grapple.state == "COLLAR_TIE"
            and game.grapple.control == "green"
            and in_range(green, red, 160)
        ):
            award_points(green, 5)
            green.cooldown = ATTACK_COOLDOWN_FRAMES + 30
            game.last_action_text = "Green suplex!"
            game.last_points_text = "+5"
            animation.start_cutaway("green_5pt")
            game.grapple.start_top_bottom("green")
        return

    if event.key == pygame.K_k and red.cooldown == 0:
        if (
            game.grapple.state == "COLLAR_TIE"
            and game.grapple.control == "red"
            and in_range(red, green, 180)
        ):
            award_points(red, 4)
            red.cooldown = ATTACK_COOLDOWN_FRAMES + 20
            game.last_action_text = "Red 4-point throw!"
            game.last_points_text = "+4"
            animation.start_cutaway("red_4pt")
            game.grapple.start_top_bottom("red")
        else:
            game.last_action_text = "Red needs tie control for the throw"
            game.last_points_text = ""
        return

    if event.key == pygame.K_l and red.cooldown == 0:
        if (
            game.grapple.state == "COLLAR_TIE"
            and game.grapple.control == "red"
            and in_range(red, green, 160)
        ):
            award_points(red, 5)
            red.cooldown = ATTACK_COOLDOWN_FRAMES + 30
            game.last_action_text = "Red suplex!"
            game.last_points_text = "+5"
            animation.start_cutaway("red_5pt")
            game.grapple.start_top_bottom("red")
        return
