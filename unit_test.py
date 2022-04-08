""" Unit tests """
import unittest
from unittest.mock import patch
from NBA_API import get_player_id, get_player_games_between_dates
import pandas as pd


def lebron_id(name):
    return 2544


class GetPlayerIdTests(unittest.TestCase):
    """Tests the get_player_id function"""

    def test_none(self):
        """Unit test to see if func returns none if input is none"""
        self.assertEqual(get_player_id(None), None)

    def test_empty_string(self):
        """Unit test to see if funct returns none if input is an empty string"""
        self.assertEqual(get_player_id(""), None)

    def test_fake_name(self):
        """Unit test to see if funct returns none if input is a player whose name doesn't exist"""
        self.assertEqual(get_player_id("ngmjskfdngfjksa"), None)

    def test_real_name(self):
        """Unit test to see if funct returns player's name if input is valid player id"""
        self.assertEqual(get_player_id("Lebron James"), 2544)


class GetPlayerGamesTests(unittest.TestCase):
    """Tests the get_player_games_between_dates function"""

    def test_none(self):
        """Unit test to see if func returns none if id is none"""
        self.assertEqual(
            get_player_games_between_dates("12/25/2020", "12/25/2021", None), None
        )

    def test_fake_player_id(self):
        """Unit test to see if func returns there are no games if id doesn't exist"""
        self.assertEqual(
            get_player_games_between_dates("12/25/2020", "12/25/2021", "1000000"),
            "No games for this player during time",
        )

    def test_reversed_to_from_dates(self):
        """Unit test to see if func returns there are no games if input is from is later than to"""
        self.assertEqual(
            get_player_games_between_dates("12/25/2021", "12/25/2020", "2544"),
            "No games for this player during time",
        )


if __name__ == "__main__":
    unittest.main()
