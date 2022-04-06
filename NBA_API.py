from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players

player_info = commonplayerinfo.CommonPlayerInfo(player_id=2544)
playerdict = player_info.player_headline_stats.get_dict()
print(playerdict)
print(playerdict["data"][0][0])
Players = players.find_players_by_full_name("James Anderson")
test = Players[0]
print(Players[0])
print(test["id"])


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
