from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd

""""
Meant for testing code will delete later
player_info = commonplayerinfo.CommonPlayerInfo(player_id=2544)
playerdict = player_info.player_headline_stats.get_dict()
print(playerdict)
print(playerdict["data"][0][0])
Players = players.find_players_by_full_name("Lebron James")
test = Players[0]
print(Players)
print(test["id"])
gamelog_bron_all = playergamelog.PlayerGameLog(player_id="2544")
df_bron_games_all = gamelog_bron_all.get_dict()
##print(df_bron_games_all["resultSets"][0]["rowSet"][0])
gamelog_bron_all = playergamelog.PlayerGameLog(player_id="2544", season=SeasonAll.all)
df_bron_games_all = gamelog_bron_all.get_dict()
##print(df_bron_games_all)
gamelog_bron_all = playergamelog.PlayerGameLog(
    player_id="2544", date_from_nullable="12/25/2020", date_to_nullable="12/25/2021"
)
df_bron_games_all = gamelog_bron_all.get_data_frames()
df = pd.DataFrame(df_bron_games_all[0])
df2 = df["PTS"].mean()
##print(df_bron_games_all)
df.plot(x="AST", y="PTS", kind="scatter")
print(plt.get_backend())
plt.show(block=True)
print(df2)
"""



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
    return ("Name:",name, "Time Frame:",time_frame, "Points:",pts, "Assists:",ast, "Rebounds:",reb, pie)


def get_player_games_between_dates(date_from, date_to, player_id):
    """Function to return panda dataframe with info from all games a player has played from and to specific dates"""
    if None in (date_from, date_to, player_id):
        return None
    gamelog_all = playergamelog.PlayerGameLog(
        player_id=player_id, date_from_nullable=date_from, date_to_nullable=date_to
    )
    games_all = gamelog_all.get_data_frames()
    df = pd.DataFrame(games_all[0])
    if df.empty:
        return "No games for this player during time"
    return df

print(get_player_info(get_player_id("Trae Young")))
