import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from computer_helpers import generate_all_tapping_moves, generate_all_distribute_moves


class TestGenerateAllTappingMoves(unittest.TestCase):
    """Test cases for generate_all_tapping_moves function"""

    def test_both_hands_alive(self):
        """Test when both players have both hands alive"""
        hero_state = (1, 2)
        opponent_state = (3, 4)
        result = generate_all_tapping_moves(hero_state, opponent_state)
        # Hero hand 0 (1) can tap opponent hands 0 (3) and 1 (4)
        # Hero hand 1 (2) can tap opponent hands 0 (3) and 1 (4)
        expected = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.assertEqual(result, expected)

    def test_hero_left_hand_dead(self):
        """Test when hero's left hand is dead (0)"""
        hero_state = (0, 2)
        opponent_state = (1, 3)
        result = generate_all_tapping_moves(hero_state, opponent_state)
        # Only hero hand 1 can tap
        expected = [(1, 0), (1, 1)]
        self.assertEqual(result, expected)

    def test_hero_right_hand_dead(self):
        """Test when hero's right hand is dead (0)"""
        hero_state = (2, 0)
        opponent_state = (1, 3)
        result = generate_all_tapping_moves(hero_state, opponent_state)
        # Only hero hand 0 can tap
        expected = [(0, 0), (0, 1)]
        self.assertEqual(result, expected)

    def test_opponent_left_hand_dead(self):
        """Test when opponent's left hand is dead (0)"""
        hero_state = (1, 2)
        opponent_state = (0, 3)
        result = generate_all_tapping_moves(hero_state, opponent_state)
        # Can only tap opponent hand 1
        expected = [(0, 1), (1, 1)]
        self.assertEqual(result, expected)

    def test_opponent_right_hand_dead(self):
        """Test when opponent's right hand is dead (0)"""
        hero_state = (1, 2)
        opponent_state = (3, 0)
        result = generate_all_tapping_moves(hero_state, opponent_state)
        # Can only tap opponent hand 0
        expected = [(0, 0), (1, 0)]
        self.assertEqual(result, expected)

    def test_both_hero_hands_dead(self):
        """Test when both hero hands are dead"""
        hero_state = (0, 0)
        opponent_state = (1, 2)
        result = generate_all_tapping_moves(hero_state, opponent_state)
        # No moves possible
        expected = []
        self.assertEqual(result, expected)

    def test_both_opponent_hands_dead(self):
        """Test when both opponent hands are dead"""
        hero_state = (1, 2)
        opponent_state = (0, 0)
        result = generate_all_tapping_moves(hero_state, opponent_state)
        # No moves possible
        expected = []
        self.assertEqual(result, expected)

    def test_multiple_dead_hands(self):
        """Test when both players have one dead hand"""
        hero_state = (0, 3)
        opponent_state = (2, 0)
        result = generate_all_tapping_moves(hero_state, opponent_state)
        # Only hero hand 1 can tap opponent hand 0
        expected = [(1, 0)]
        self.assertEqual(result, expected)


class TestGenerateAllDistributeMoves(unittest.TestCase):
    """Test cases for generate_all_distribute_moves function"""

    def test_distribute_two_fingers(self):
        """Test distributing 2 fingers"""
        hero_state = (0, 2)
        result = generate_all_distribute_moves(hero_state)
        # Total = 2, possible: (1, 1)
        # Excluding original (0, 2)
        expected = [(1, 1)]
        self.assertEqual(result, expected)

    def test_distribute_three_fingers(self):
        """Test distributing 3 fingers"""
        hero_state = (0, 3)
        result = generate_all_distribute_moves(hero_state)
        # Total = 3, possible: (1, 2)
        # Excluding original (0, 3)
        expected = [(1, 2)]
        self.assertEqual(result, expected)

    def test_distribute_four_fingers(self):
        """Test distributing 4 fingers"""
        hero_state = (0, 4)
        result = generate_all_distribute_moves(hero_state)
        # Total = 4, possible: (0, 4), (1, 3), (2, 2)
        # Excluding original (0, 4)
        expected = [(1, 3), (2, 2)]
        self.assertEqual(result, expected)

    def test_distribute_from_balanced_state(self):
        """Test distributing from already balanced state"""
        hero_state = (2, 2)
        result = generate_all_distribute_moves(hero_state)
        # Total = 4, possible: (0, 4), (1, 3), (2, 2)
        # Excluding original (2, 2)
        expected = [(0, 4), (1, 3)]
        self.assertEqual(result, expected)

    def test_distribute_five_fingers(self):
        """Test distributing 5 fingers"""
        hero_state = (1, 4)
        result = generate_all_distribute_moves(hero_state)
        # Total = 5, possible: (1, 4), (2, 3)
        # Excluding original (1, 4)
        expected = [(2, 3)]
        self.assertEqual(result, expected)

    def test_distribute_six_fingers(self):
        """Test distributing 6 fingers"""
        hero_state = (2, 4)
        result = generate_all_distribute_moves(hero_state)
        # Total = 6, possible: (2, 4), (3, 3)
        # Excluding original (2, 4)
        expected = [(3, 3)]
        self.assertEqual(result, expected)

    def test_distribute_seven_fingers(self):
        """Test distributing 7 fingers"""
        hero_state = (3, 4)
        result = generate_all_distribute_moves(hero_state)
        # Total = 7, possible: (3, 4)
        # Excluding original (3, 4) - no other valid distributions
        expected = []
        self.assertEqual(result, expected)

    def test_distribute_eight_fingers(self):
        """Test distributing 8 fingers (maximum)"""
        hero_state = (4, 4)
        result = generate_all_distribute_moves(hero_state)
        # Total = 8, possible: (4, 4)
        # Excluding original (4, 4) - no other valid distributions
        expected = []
        self.assertEqual(result, expected)

    def test_distribute_with_reversed_input(self):
        """Test that function normalizes input (min, max)"""
        hero_state = (3, 1)
        result = generate_all_distribute_moves(hero_state)
        # Total = 4, normalized to (1, 3)
        # Possible: (0, 4), (1, 3), (2, 2)
        # Excluding original (1, 3)
        expected = [(0, 4), (2, 2)]
        self.assertEqual(result, expected)

    def test_distribute_one_finger(self):
        """Test distributing with only 1 finger total"""
        hero_state = (0, 1)
        result = generate_all_distribute_moves(hero_state)
        # Total = 1, only possible: (0, 1)
        # Excluding original (0, 1)
        expected = []
        self.assertEqual(result, expected)

    def test_distribute_unbalanced_state(self):
        """Test distributing from unbalanced state"""
        hero_state = (1, 3)
        result = generate_all_distribute_moves(hero_state)
        # Total = 4, possible: (0, 4), (1, 3), (2, 2)
        # Excluding original (1, 3)
        expected = [(0, 4), (2, 2)]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
