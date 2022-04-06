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
