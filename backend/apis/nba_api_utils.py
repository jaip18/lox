from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playergamelog
from nba_api.live.nba.endpoints import scoreboard


def fetch_active_players():
    nba_players = players.get_active_players()  # List of all active players
    return nba_players  # <- return the list for later use (e.g., storing in DB)


def fetch_player_info(id):
    player = commonplayerinfo.CommonPlayerInfo(player_id=id)
    info = player.get_normalized_dict()

    # Extract commonly used fields
    player_data = info['CommonPlayerInfo'][0]
    return {
        'player_id': player_data['PERSON_ID'],
        'name': player_data['DISPLAY_FIRST_LAST'],
        'team_name': player_data['TEAM_NAME'],
        'position': player_data['POSITION'],
        'height': player_data['HEIGHT'],
        'weight': player_data['WEIGHT'],
        'birth_date': player_data['BIRTHDATE'],
        'school': player_data['SCHOOL'],
        'country': player_data['COUNTRY'],
        'jersey_number': player_data['JERSEY'],
        'from_year': player_data['FROM_YEAR'],
        'to_year': player_data['TO_YEAR'],
        'draft_year': player_data['DRAFT_YEAR'],
        'draft_round': player_data['DRAFT_ROUND'],
        'draft_number': player_data['DRAFT_NUMBER']
    }


def fetch_player_stats(id):
    player = commonplayerinfo.CommonPlayerInfo(player_id=id)
    stats = player.get_normalized_dict()

    headline = stats['PlayerHeadlineStats'][0]
    return {
        'points': headline['PTS'],
        'rebounds': headline['REB'],
        'assists': headline['AST']
    }


def fetch_player_game_logs(id):
    logs = playergamelog.PlayerGameLog(player_id=id)
    data = logs.get_normalized_dict()
    gamelogs = data['PlayerGameLog']
    return gamelogs  # return list of dictionaries


def fetch_games():
    games = scoreboard.ScoreBoard()
    data = games.get_dict()
    return data['scoreboard']['games']  # return list of today’s games









