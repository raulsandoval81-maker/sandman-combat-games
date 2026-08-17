import unittest
from unittest.mock import Mock, patch

from game.game import WrestlingGame
from game.grapple import GrappleState
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
