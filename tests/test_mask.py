import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
from agents.dqn_agent import getValidMoveMask, mask_idx_to_action
from custom_types import Actions


class TestMaskIdxToAction(unittest.TestCase):
    """Test cases for mask_idx_to_action function"""

    def test_split_actions(self):
        self.assertEqual(mask_idx_to_action(3), (Actions.split, (0, 3)))
        self.assertEqual(mask_idx_to_action(7), (Actions.split, (1, 2)))
        self.assertEqual(mask_idx_to_action(24), (Actions.split, (4, 4)))

    def test_tap_actions(self):
        self.assertEqual(mask_idx_to_action(25), (Actions.tap, (0, 0)))
        self.assertEqual(mask_idx_to_action(26), (Actions.tap, (0, 1)))
        self.assertEqual(mask_idx_to_action(27), (Actions.tap, (1, 0)))
        self.assertEqual(mask_idx_to_action(28), (Actions.tap, (1, 1)))


class TestGetValidMoveMask(unittest.TestCase):
    """Test cases for getValidMoveMask function"""

    def test_standard_game_position(self):
        """Happy path: Both players have both hands alive with different values"""
        game_position = ((1, 2), (3, 1))
        result = getValidMoveMask(game_position)

        expected = torch.zeros(50)
        expected[3] = 1   # split (0,3)
        expected[15] = 1  # split (3,0)
        expected[25] = 1  # tap: hero hand 0 -> opp hand 0
        expected[26] = 1  # tap: hero hand 0 -> opp hand 1
        expected[27] = 1  # tap: hero hand 1 -> opp hand 0
        expected[28] = 1  # tap: hero hand 1 -> opp hand 1

        self.assertTrue(torch.equal(result, expected))

    def test_hero_one_hand_dead(self):
        """Edge case: Hero's left hand is dead (0)"""
        game_position = ((0, 3), (2, 1))
        result = getValidMoveMask(game_position)

        expected = torch.zeros(50)
        expected[7] = 1   # split (1,2)
        expected[11] = 1  # split (2,1)
        expected[27] = 1  # tap: hero hand 1 -> opp hand 0
        expected[28] = 1  # tap: hero hand 1 -> opp hand 1

        self.assertTrue(torch.equal(result, expected))

    def test_opponent_one_hand_dead(self):
        """Edge case: Opponent's right hand is dead"""
        game_position = ((2, 2), (3, 0))
        result = getValidMoveMask(game_position)

        expected = torch.zeros(50)
        expected[4] = 1   # split (0,4)
        expected[8] = 1   # split (1,3)
        expected[16] = 1  # split (3,1)
        expected[20] = 1  # split (4,0)
        expected[25] = 1  # tap: hero hand 0 -> opp hand 0
        expected[27] = 1  # tap: hero hand 1 -> opp hand 0

        self.assertTrue(torch.equal(result, expected))

    def test_both_hero_hands_dead(self):
        """Edge case: Both hero hands are dead - no taps possible"""
        game_position = ((0, 0), (1, 2))
        result = getValidMoveMask(game_position)

        expected = torch.zeros(50)
        # No valid splits (total=0, only (0,0) possible which is original)
        # No valid taps (both hero hands dead)

        self.assertTrue(torch.equal(result, expected))

    def test_no_valid_splits(self):
        """Edge case: Only one finger total - no valid splits possible"""
        game_position = ((0, 1), (2, 2))
        result = getValidMoveMask(game_position)

        expected = torch.zeros(50)
        # No valid splits (total=1, only (0,1) and (1,0) which is swap)
        expected[27] = 1  # tap: hero hand 1 -> opp hand 0
        expected[28] = 1  # tap: hero hand 1 -> opp hand 1

        self.assertTrue(torch.equal(result, expected))

    def test_max_fingers_no_split(self):
        """Edge case: Maximum fingers (4,4) - no other valid distributions"""
        game_position = ((4, 4), (1, 1))
        result = getValidMoveMask(game_position)

        expected = torch.zeros(50)
        # No valid splits (total=8, only (4,4) possible which is original)
        expected[25] = 1  # tap: hero hand 0 -> opp hand 0
        expected[26] = 1  # tap: hero hand 0 -> opp hand 1
        expected[27] = 1  # tap: hero hand 1 -> opp hand 0
        expected[28] = 1  # tap: hero hand 1 -> opp hand 1

        self.assertTrue(torch.equal(result, expected))


if __name__ == '__main__':
    unittest.main()
