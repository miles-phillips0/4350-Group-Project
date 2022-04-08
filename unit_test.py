import unittest
from unittest.mock import patch
from NBA_API import get_player_id, get_player_games_between_dates


class GetPlayerIdTests(unittest.TestCase):
    """Tests the get_player_id function"""

    def test_none(self):
        self.assertEqual(get_player_id(None), None)

    def test_empty_string(self):
        self.assertEqual(get_player_id(""), None)

    def test_fake_name(self):
        self.assertEqual(get_player_id("ngmjskfdngfjksa"), None)

    def test_real_name(self):
        self.assertEqual(get_player_id("Lebron James"), 2544)


class GetPlayerGamesTests(unittest.TestCase):
    def test_none(self):
        self.assertEqual(
            get_player_games_between_dates("12/25/2020", "12/25/2021", None), None
        )

    def test_fake_player_id(self):
        self.assertEqual(
            get_player_games_between_dates("12/25/2020", "12/25/2021", "1000000"),
            "No games for this player during time",
        )

    def test_reversed_to_from_dates(self):
        self.assertEqual(
            get_player_games_between_dates("12/25/2021", "12/25/2020", "2544"),
            "No games for this player during time",
        )


""""
def nonrandom_choice(movie_ids):
    return movie_ids[0]
class getMovieUrlTests(unittest.TestCase):
    def test_none(self):
        self.assertEqual(get_movie_url(None), None)

    def test_one_movie(self):
        input_id = ["15923"]
        expected_output = "https://api.themoviedb.org/3/movie/15923"
        actual_output = get_movie_url(input_id)
        self.assertEqual(expected_output, actual_output)

    def test_get_movie_ids(self):
        movie_ids = ["123", "456", "789"]
        with patch("activity.random.choice", nonrandom_choice):
            expected_output = BASE_URL + "123"
            self.assertEqual(get_movie_url(movie_ids), expected_output)
"""

# class getMovieUrlTests(unittest.TestCase):
#    def test_emptyurl(self):
#       self.assertEqual(get_movie_genres(None), None)
if __name__ == "__main__":
    unittest.main()
