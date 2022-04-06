from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.endpoints import playergamelog

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
print(df_bron_games_all["resultSets"][0]["rowSet"][0])
gamelog_bron_all = playergamelog.PlayerGameLog(player_id="2544", season=SeasonAll.all)
df_bron_games_all = gamelog_bron_all.get_dict()
##print(df_bron_games_all)
gamelog_bron_all = playergamelog.PlayerGameLog(
    player_id="2544", date_from_nullable="12/25/2020", date_to_nullable="12/25/2021"
)
df_bron_games_all = gamelog_bron_all.get_dict()
print(df_bron_games_all)


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
