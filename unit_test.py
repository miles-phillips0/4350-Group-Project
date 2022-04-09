""" Unit tests """
import unittest
from unittest.mock import patch
from NBA_API import get_player_id, get_player_games_between_dates


def lebron(name):
    # pylint: disable=unused-argument
    """mock function to return what it should return if lebron was searched by API"""
    return [
        {
            "id": 2544,
            "full_name": "LeBron James",
            "first_name": "LeBron",
            "last_name": "James",
            "is_active": True,
        }
    ]


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
        """Unit test to see if funct returns player's id if input is valid player name"""
        self.assertEqual(get_player_id("Lebron James"), 2544)

    with patch("NBA_API.players.find_players_by_full_name", lebron):

        def test_mock_real_name(self):
            """Unit test to see if funct returns player's id if input is valid player name"""
            self.assertEqual(get_player_id("Lebron James"), 2544)

        def test_mock_close_name(self):
            """Unit test to see if funct returns player's id if input is close to valid player name"""
            self.assertEqual(get_player_id("Lebron Ja"), 2544)


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
