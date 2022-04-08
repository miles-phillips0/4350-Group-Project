from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import matplotlib.pyplot as plt

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
    playersList = players.find_players_by_full_name(name)
    player = playersList[0]
    return player["id"]


def get_player_info(id):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=id)
    playerdict = player_info.player_headline_stats.get_dict()
    name = playerdict["data"][0][1]
    time_frame = playerdict["data"][0][2]
    pts = playerdict["data"][0][3]
    ast = playerdict["data"][0][4]
    reb = playerdict["data"][0][5]
    pie = playerdict["data"][0][6]
    return (name, time_frame, pts, ast, reb, pie)


def get_player_games_between_dates(date_from, date_to, id):
    gamelog_all = playergamelog.PlayerGameLog(
        player_id=id, date_from_nullable=date_from, date_to_nullable=date_to
    )
    games_all = gamelog_all.get_data_frames()
    df = pd.DataFrame(games_all[0])
    return df
