import unittest
from unittest.mock import Mock, patch

from game.game import WrestlingGame
from game.grapple import GrappleState, SCRAMBLE, TOP_BOTTOM, SNAP_SHOT_FRAMES
from game.player import Player
from game.scoring import check_tech_fall


class CombatRuleTests(unittest.TestCase):
    def test_technical_fall_uses_score_difference(self):
        green = Player("green", (0, 0))
        red = Player("red", (0, 0))
        green.score, red.score = 10, 9
        self.assertIsNone(check_tech_fall(green, red))
        green.score = 19
        self.assertEqual(check_tech_fall(green, red), "GREEN WINS!")

    def test_only_one_turn_scores_per_top_possession(self):
        grapple = GrappleState()
        grapple.start_top_bottom("green")
        self.assertTrue(grapple.record_turn("green"))
        self.assertFalse(grapple.record_turn("green"))
        self.assertFalse(grapple.can_turn("red"))

    def test_top_bottom_locks_free_movement(self):
        grapple = GrappleState()
        grapple.start_top_bottom("red")
        self.assertEqual(grapple.movement_speed(), 0)

    def test_hand_fight_requires_progress_before_inside_control(self):
        grapple = GrappleState()
        grapple.state = "CONTACT"

        self.assertTrue(grapple.hand_fight("green"))
        self.assertEqual(grapple.control_progress("green"), (1, 3))
        self.assertIsNone(grapple.control)

        grapple.hand_fight("green")
        self.assertEqual(grapple.control_progress("green"), (2, 3))
        self.assertIsNone(grapple.control)

        grapple.hand_fight("green")
        self.assertEqual(grapple.control_progress("green"), (3, 3))
        self.assertEqual(grapple.state, "COLLAR_TIE")
        self.assertEqual(grapple.control, "green")

    def test_counter_hand_fight_strips_existing_tie_control(self):
        grapple = GrappleState()
        grapple.state = "CONTACT"
        for _ in range(3):
            grapple.hand_fight("green")

        self.assertEqual(grapple.control, "green")
        self.assertTrue(grapple.hand_fight("red"))
        self.assertEqual(grapple.state, "CONTACT")
        self.assertIsNone(grapple.control)
        self.assertEqual(grapple.control_progress("green"), (2, 3))
        self.assertEqual(grapple.control_progress("red"), (1, 3))

    def test_contact_shot_enters_scramble_then_takedown(self):
        grapple = GrappleState()
        grapple.state = "CONTACT"

        self.assertTrue(grapple.start_shot("green"))
        self.assertEqual(grapple.state, SCRAMBLE)

        for _ in range(20):
            grapple._tick_scramble()

        resolution = grapple.consume_resolution()
        self.assertEqual(resolution["outcome"], "takedown")
        self.assertEqual(resolution["attacker"], "green")
        self.assertEqual(grapple.state, TOP_BOTTOM)
        self.assertEqual(grapple.top_wrestler, "green")

    def test_defender_can_sprawl_during_shot_window(self):
        grapple = GrappleState()
        grapple.state = "CONTACT"

        self.assertTrue(grapple.start_shot("green"))
        self.assertTrue(grapple.attempt_sprawl("red"))
        self.assertFalse(grapple.attempt_sprawl("green"))

        for _ in range(20):
            grapple._tick_scramble()

        resolution = grapple.consume_resolution()
        self.assertEqual(resolution["outcome"], "sprawl")
        self.assertEqual(resolution["defender"], "red")
        self.assertEqual(grapple.state, "CONTACT")
        self.assertEqual(grapple.control, "red")

    def test_snap_down_shortens_shot_window_but_keeps_sprawl_available(self):
        grapple = GrappleState()
        grapple.state = "CONTACT"
        for _ in range(3):
            grapple.hand_fight("green")

        self.assertFalse(grapple.snap_down("red"))
        self.assertTrue(grapple.snap_down("green"))
        self.assertTrue(grapple.start_shot("green"))
        self.assertEqual(grapple.scramble_timer, SNAP_SHOT_FRAMES)
        self.assertTrue(grapple.attempt_sprawl("red"))
        for _ in range(SNAP_SHOT_FRAMES):
            grapple._tick_scramble()
        self.assertEqual(grapple.consume_resolution()["outcome"], "sprawl")

    def test_snap_opening_expires_or_is_stripped_by_counter(self):
        grapple = GrappleState()
        grapple.state = "CONTACT"
        for _ in range(3):
            grapple.hand_fight("green")
        grapple.snap_down("green")
        grapple.hand_fight("red")
        self.assertIsNone(grapple.snap_setup)

        for _ in range(2):
            grapple.hand_fight("green")
        grapple.snap_down("green")
        grapple.snap_timer = 1
        green = Player("green", (500, 400))
        red = Player("red", (580, 400))
        grapple.update(green, red)
        self.assertIsNone(grapple.snap_setup)
        grapple.start_shot("green")
        self.assertEqual(grapple.scramble_timer, 20)

    def test_cutaway_locks_held_movement_for_both_players(self):
        game = WrestlingGame.__new__(WrestlingGame)
        game.mode = "playing"
        game.game_over = False
        game.green = Player("green", (100, 100))
        game.red = Player("red", (200, 200))
        game.animation = Mock(cutaway_timer=10)
        game.grapple = Mock()
        game.timer = Mock()
        game.timer.is_finished.return_value = False
        starting_positions = (game.green.x, game.green.y, game.red.x, game.red.y)

        def move_both_players(*_args):
            game.green.x += 5
            game.green.y += 5
            game.red.x -= 5
            game.red.y -= 5

        with patch("game.game.handle_movement", side_effect=move_both_players) as movement:
            game.update()

        movement.assert_not_called()
        self.assertEqual(
            (game.green.x, game.green.y, game.red.x, game.red.y),
            starting_positions,
        )


if __name__ == "__main__":
    unittest.main()
