"""File with functions to handle nba_api calls"""
# pylint: disable=invalid-name
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import numpy



def get_player_id(name):
    """Function to search for player's id using NBA_API with a string as input"""
    if name is not None and len(name) > 0:
        players_list = players.find_players_by_full_name(name)
        if not players_list:
            # Checks if list is empty and if it is returns None
            return None

        return players_list[0]["id"]
    return None


def get_player_info(player_id):
    """Function to return HeadLine data for specific player id"""
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    playerdict = player_info.player_headline_stats.get_dict()
    name = playerdict["data"][0][1]
    time_frame = playerdict["data"][0][2]
    pts = playerdict["data"][0][3]
    ast = playerdict["data"][0][4]
    reb = playerdict["data"][0][5]
    pie = playerdict["data"][0][6]
    return (name ,time_frame ,pts ,ast ,reb, pie)


def get_player_games_between_dates(date_from, date_to, player_id):
    """Function to return panda dataframe of all games a player has played between dates"""
    if None in (date_from, date_to, player_id):
        return None
    gamelog_all = playergamelog.PlayerGameLog(
        player_id=player_id, date_from_nullable=date_from, date_to_nullable=date_to
    )
    games_all = gamelog_all.get_data_frames()
    pd_df = pd.DataFrame(games_all[0])
    if pd_df.empty:
        return "No games for this player during time"
    return pd_df
