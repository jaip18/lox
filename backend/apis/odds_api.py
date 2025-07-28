import requests
from datetime import datetime, timezone


BASE_URL = 'https://api.sportsgameodds.com/v2'

headers = {
    'X-Api-Key': '58e3f7b9080bc769ab3ff334bc46f044'
}

SPORTS_URL = f'{BASE_URL}/sports/'
LEAGUE_URL = f'{BASE_URL}/leagues/'
EVENT_URL = f'{BASE_URL}/events/'
ODDS_URL = f'{BASE_URL}/odds/'


today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")


def fetch_all_sports():
    try:
        response = requests.get(SPORTS_URL, headers=headers) 
        response.raise_for_status()

        data = response.json()
        sports = data['data']
        return sports
    
    except requests.Timeout:
        print("⚠️ Timeout: The request to SportsGameOdds took too long.")
    except requests.RequestException as e:
        print(f"⚠️ Request error: {e}")
    except ValueError:
        print("⚠️ JSON decoding failed.")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

    return []


def fetch_all_leagues():
    try:
        response = requests.get(LEAGUE_URL, headers=headers) 
        response.raise_for_status()

        data = response.json()
        leagues = data['data']
        return leagues
    
    except requests.Timeout:
        print("⚠️ Timeout: The request to SportsGameOdds took too long.")
    except requests.RequestException as e:
        print(f"⚠️ Request error: {e}")
    except ValueError:
        print("⚠️ JSON decoding failed.")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

    return []


def fetch_league_by_ID(leagueID):
    leagues = fetch_all_leagues()
    for league in leagues:
        if league['leagueID'] == leagueID:
            return league

    return None


def fetch_current_events_by_league(leagueID, startsAfter):
    try:
        params = {
            "startsAfter": startsAfter,
            "leagueID": leagueID,
        }
        response = requests.get(EVENT_URL, headers=headers, params=params) 
        response.raise_for_status()

        data = response.json()
        events = data['data']
        return events
    
    except requests.Timeout:
        print("⚠️ Timeout: The request to SportsGameOdds took too long.")
    except requests.RequestException as e:
        print(f"⚠️ Request error: {e}")
    except ValueError:
        print("⚠️ JSON decoding failed.")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

    return []


def fetch_event_by_eventID(eventID):
    try:
        params = {
            "eventID": eventID,
        }
        response = requests.get(EVENT_URL, headers=headers, params=params) 
        response.raise_for_status()

        data = response.json()
        events = data['data']
        return events
    
    except requests.Timeout:
        print("⚠️ Timeout: The request to SportsGameOdds took too long.")
    except requests.RequestException as e:
        print(f"⚠️ Request error: {e}")
    except ValueError:
        print("⚠️ JSON decoding failed.")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

    return []


def fetch_odds_by_event(eventID):
    try:
        params = {
            "eventID": eventID,
            "region": "us",
        }
        response = requests.get(ODDS_URL, headers=headers, params=params) 
        response.raise_for_status()

        data = response.json()
        odds = data['data']
        return odds
    
    except requests.Timeout:
        print("⚠️ Timeout: The request to SportsGameOdds took too long.")
    except requests.RequestException as e:
        print(f"⚠️ Request error: {e}")
    except ValueError:
        print("⚠️ JSON decoding failed.")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

    return []


def extract_matchup_names(event):
    try:
        home = event['teams']['home']['names']['long']
        away = event['teams']['away']['names']['long']
        return f"{home} vs {away}"
    except KeyError:
        return "Unknown Matchup"
    

def fetch_limits():
    try:
        response = requests.get('https://api.sportsgameodds.com/v2/account/usage', headers=headers) 
        response.raise_for_status()

        data = response.json()
        limits = data['data']
        return limits
    
    except requests.Timeout:
        print("⚠️ Timeout: The request to SportsGameOdds took too long.")
    except requests.RequestException as e:
        print(f"⚠️ Request error: {e}")
    except ValueError:
        print("⚠️ JSON decoding failed.")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

    return []





