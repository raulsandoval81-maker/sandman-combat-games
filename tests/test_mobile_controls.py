import unittest
from collections import defaultdict
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pygame

from game.controls import handle_action_input, handle_keydown, handle_movement
from game.game import WrestlingGame
from game.grapple import CONTACT, TOP_BOTTOM, GrappleState
from game.mobile_input import MobileInput
from game.player import Player


class MobileControlTests(unittest.TestCase):
    def setUp(self):
        self.mobile = MobileInput()
        self.actions = []
        self.keys = defaultdict(bool)
        self.green = Player("green", (330, 380))
        self.red = Player("red", (720, 380))

    def test_joystick_movement_input(self):
        center_x, center_y = self.mobile.JOYSTICK_CENTER
        self.mobile.pointer_down(
            1, (center_x + 50, center_y), self.actions.append
        )
        handle_movement(
            self.keys,
            self.green,
            self.red,
            GrappleState(),
            self.mobile.joystick_vector,
        )
        self.assertGreater(self.green.x, self.green.start_x)

    def test_joystick_drag_changes_direction(self):
        center_x, center_y = self.mobile.JOYSTICK_CENTER
        self.mobile.pointer_down(1, (center_x + 40, center_y), self.actions.append)
        self.assertGreater(self.mobile.joystick_vector[0], 0)
        self.mobile.pointer_motion(1, (center_x - 40, center_y - 20))
        self.assertLess(self.mobile.joystick_vector[0], 0)
        self.assertLess(self.mobile.joystick_vector[1], 0)

    def test_joystick_release_resets_vector_and_knob(self):
        center = self.mobile.JOYSTICK_CENTER
        self.mobile.pointer_down(1, (center[0] + 40, center[1]), self.actions.append)
        self.mobile.pointer_up(1)
        self.assertEqual(self.mobile.joystick_vector, (0.0, 0.0))
        self.assertEqual(self.mobile.joystick_knob_position, center)

    def test_action_button_press_and_release(self):
        self.mobile.pointer_down(
            2, self.mobile.button_centers["triangle"], self.actions.append
        )
        self.assertEqual(self.actions, ["triangle"])
        self.assertIn("triangle", self.mobile.pressed_actions)
        self.mobile.pointer_up(2)
        self.assertNotIn("triangle", self.mobile.pressed_actions)

    def test_joystick_and_action_use_independent_touches(self):
        center_x, center_y = self.mobile.JOYSTICK_CENTER
        self.mobile.pointer_down(10, (center_x + 45, center_y), self.actions.append)
        self.mobile.pointer_down(
            11, self.mobile.button_centers["square"], self.actions.append
        )
        self.assertEqual(self.mobile.joystick_touch_id, 10)
        self.assertGreater(self.mobile.joystick_vector[0], 0)
        self.assertIn("square", self.mobile.pressed_actions)
        self.mobile.pointer_up(11)
        self.assertGreater(self.mobile.joystick_vector[0], 0)

    def test_touch_movement_respects_top_bottom_lock(self):
        grapple = GrappleState()
        grapple.start_top_bottom("green")
        center_x, center_y = self.mobile.JOYSTICK_CENTER
        self.mobile.pointer_down(1, (center_x + 50, center_y), self.actions.append)
        starting_positions = (self.green.x, self.green.y, self.red.x, self.red.y)
        handle_movement(
            self.keys,
            self.green,
            self.red,
            grapple,
            self.mobile.joystick_vector,
        )
        self.assertEqual(
            (self.green.x, self.green.y, self.red.x, self.red.y),
            starting_positions,
        )

    def test_mobile_movement_is_blocked_during_cutaway(self):
        game = self._update_game(cutaway_timer=10)
        center_x, center_y = game.mobile_input.JOYSTICK_CENTER
        game.mobile_input.pointer_down(
            1, (center_x + 50, center_y), self.actions.append
        )
        starting_positions = (game.green.x, game.green.y, game.red.x, game.red.y)
        with patch("game.game.pygame.key.get_pressed", return_value=self.keys):
            game.update()
        self.assertEqual(
            (game.green.x, game.green.y, game.red.x, game.red.y),
            starting_positions,
        )

    def test_existing_keyboard_movement_still_works(self):
        self.keys[pygame.K_d] = True
        handle_movement(self.keys, self.green, self.red, GrappleState())
        self.assertGreater(self.green.x, self.green.start_x)

    def test_existing_keyboard_action_still_works(self):
        game = self._combat_game()
        game.green.x, game.green.y = 500, 400
        game.red.x, game.red.y = 580, 400
        game.grapple.state = CONTACT
        handle_keydown(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c), game)
        self.assertEqual(game.grapple.control, "green")
        handle_keydown(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE), game)
        self.assertEqual(game.green.score, 2)
        self.assertEqual(game.grapple.top_wrestler, "green")

    def test_generic_action_is_resolved_by_control_layer(self):
        game = self._combat_game()
        game.green.x, game.green.y = 500, 400
        game.red.x, game.red.y = 580, 400
        game.grapple.state = CONTACT
        self.assertTrue(handle_action_input("triangle", game))
        self.assertEqual(game.grapple.control, "green")
        self.assertTrue(handle_action_input("square", game))
        self.assertEqual(game.green.score, 2)
        self.assertEqual(game.grapple.top_wrestler, "green")

    def _combat_game(self):
        return SimpleNamespace(
            green=self.green,
            red=self.red,
            animation=Mock(cutaway_timer=0),
            grapple=GrappleState(),
            mode="playing",
            game_over=False,
            last_action_text="",
            last_points_text="",
        )

    def _update_game(self, cutaway_timer):
        game = WrestlingGame.__new__(WrestlingGame)
        game.mode = "playing"
        game.game_over = False
        game.green = self.green
        game.red = self.red
        game.animation = Mock(cutaway_timer=cutaway_timer)
        game.grapple = GrappleState()
        game.timer = Mock()
        game.timer.is_finished.return_value = False
        game.mobile_input = MobileInput()
        return game


if __name__ == "__main__":
    unittest.main()
