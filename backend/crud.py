from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import League, NBAEvent, NBAPlayer, NBATeamOdds, NBAPlayerProps, NBAPlayerGamelogs
from datetime import datetime


def transform_event_data(event_data):
    return {
        "event_id": event_data["eventID"],
        "home_team": event_data["teams"]["home"]["names"]["long"],
        "away_team": event_data["teams"]["away"]["names"]["long"],
        "start_time": event_data["status"]["startsAt"],
        "status": event_data["status"].get("status", "scheduled")
    }


def transform_player_data(player_data):
    return {
        "player_id": str(player_data.get("PERSON_ID", player_data.get("player_id", player_data.get("id", "")))),
        "name": player_data.get("DISPLAY_FIRST_LAST", player_data.get("name", player_data.get("full_name", ""))),
        "team_name": player_data.get("TEAM_NAME", player_data.get("team_name", "")),
        "position": player_data.get("POSITION", player_data.get("position", "")),
        "height": player_data.get("HEIGHT", player_data.get("height", "")),
        "weight": player_data.get("WEIGHT", player_data.get("weight", "")),
        "birth_date": player_data.get("BIRTHDATE", player_data.get("birth_date", "")),
        "school": player_data.get("SCHOOL", player_data.get("school", "")),
        "country": player_data.get("COUNTRY", player_data.get("country", "")),
        "jersey_number": player_data.get("JERSEY", player_data.get("jersey_number", "")),
        "from_year": player_data.get("FROM_YEAR", player_data.get("from_year", "")),
        "to_year": player_data.get("TO_YEAR", player_data.get("to_year", "")),
        "draft_year": player_data.get("DRAFT_YEAR", player_data.get("draft_year", "")),
        "draft_round": player_data.get("DRAFT_ROUND", player_data.get("draft_round", "")),
        "draft_number": player_data.get("DRAFT_NUMBER", player_data.get("draft_number", ""))
    }


def transform_odds_data(odds_data, market_type="moneyline"):
    now = datetime.now()
    
    if market_type == "moneyline":
        return {
            "bookmaker": odds_data.get("bookmaker", {}).get("name", "Unknown"),
            "odds_type": "moneyline",
            "home_odds": odds_data.get("markets", {}).get("moneyline", {}).get("home", None),
            "away_odds": odds_data.get("markets", {}).get("moneyline", {}).get("away", None),
            "prop_odds": None,
            "spread": None,
            "total": None,
            "last_update": now
        }
    elif market_type == "spread":
        return {
            "bookmaker": odds_data.get("bookmaker", {}).get("name", "Unknown"),
            "odds_type": "spread",
            "home_odds": odds_data.get("markets", {}).get("spread", {}).get("home", {}).get("odds", None),
            "away_odds": odds_data.get("markets", {}).get("spread", {}).get("away", {}).get("odds", None),
            "prop_odds": None,
            "spread": odds_data.get("markets", {}).get("spread", {}).get("home", {}).get("point", None),
            "total": None,
            "last_update": now
        }
    elif market_type == "total":
        return {
            "bookmaker": odds_data.get("bookmaker", {}).get("name", "Unknown"),
            "odds_type": "total",
            "home_odds": odds_data.get("markets", {}).get("total", {}).get("over", {}).get("odds", None),
            "away_odds": odds_data.get("markets", {}).get("total", {}).get("under", {}).get("odds", None),
            "prop_odds": None,
            "spread": None,
            "total": odds_data.get("markets", {}).get("total", {}).get("point", None),
            "last_update": now
        }
    else:
        return {
            "bookmaker": odds_data.get("bookmaker", {}).get("name", "Unknown"),
            "odds_type": market_type,
            "home_odds": None,
            "away_odds": None,
            "prop_odds": None,
            "spread": None,
            "total": None,
            "last_update": now
        }


def transform_prop_data(prop_data):
    now = datetime.now()
    
    return {
        "bookmaker": prop_data.get("bookmaker", "Unknown"),
        "prop_type": prop_data.get("propType", "unknown"),
        "over_odds": prop_data.get("over", {}).get("odds", 0),
        "under_odds": prop_data.get("under", {}).get("odds", 0),
        "line": prop_data.get("line", 0),
        "last_update": now
    }


def transform_gamelog_data(gamelog_data):
    return {
        "player_id": gamelog_data.get("Player_ID", ""),
        "game_id": str(gamelog_data.get("Game_ID", "")),
        "game_date": gamelog_data.get("GAME_DATE", ""),
        "minutes": gamelog_data.get("MIN", 0),
        "field_goals_made": gamelog_data.get("FGM", 0),
        "field_goal_attempts": gamelog_data.get("FGA", 0),
        "field_goal_percent": gamelog_data.get("FG_PCT", 0.0),
        "three_pt_made": gamelog_data.get("FG3M", 0),
        "three_pt_attempts": gamelog_data.get("FG3A", 0),
        "three_pt_percent": gamelog_data.get("FG3_PCT", 0.0),
        "free_throw_made": gamelog_data.get("FTM", 0),
        "free_throw_attempts": gamelog_data.get("FTA", 0),
        "free_throw_percent": gamelog_data.get("FT_PCT", 0.0),
        "offensive_rebound": gamelog_data.get("OREB", 0),
        "defensive_rebound": gamelog_data.get("DREB", 0),
        "rebounds": gamelog_data.get("REB", 0),
        "assists": gamelog_data.get("AST", 0),
        "steals": gamelog_data.get("STL", 0),
        "blocks": gamelog_data.get("BLK", 0),
        "turnovers": gamelog_data.get("TOV", 0),
        "personal_fouls": gamelog_data.get("PF", 0),
        "points": gamelog_data.get("PTS", 0),
        "plus_minus": float(gamelog_data.get("PLUS_MINUS", 0))
    }


def extract_matchup_names(event):
    try:
        home = event['teams']['home']['names']['long']
        away = event['teams']['away']['names']['long']
        return f"{home} vs {away}"
    except KeyError:
        return "Unknown Matchup"


def create_league(db: Session, league_data: dict):
    try:
        existing_league = db.query(League).filter_by(
            league_id=league_data["leagueID"],
        ).first()

        if existing_league:
            return existing_league

        league = League(
            league_id=league_data["leagueID"],
            name=league_data["name"],
            sport=league_data.get("sportID", "UNKNOWN")
        )
        db.add(league)
        db.commit()
        db.refresh(league)
        return league
    except IntegrityError:
        db.rollback()
        return db.query(League).filter_by(league_id=league_data["leagueID"]).first()
    except Exception as e:
        db.rollback()
        raise e


def get_league_by_id(db: Session, league_id: str):
    return db.query(League).filter(League.league_id == league_id).first()


def create_NBAevent(db: Session, event_data: dict, league_id: int):
    try:
        existing_event = db.query(NBAEvent).filter_by(
            event_id=event_data["eventID"],
        ).first()

        if existing_event:
            return existing_event
        
        transformed_data = transform_event_data(event_data)
        
        event = NBAEvent(
            league_id=league_id,
            **transformed_data
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
    except IntegrityError:
        db.rollback()
        return db.query(NBAEvent).filter_by(event_id=event_data["eventID"]).first()
    except Exception as e:
        db.rollback()
        raise e


def get_NBAevent_by_id(db: Session, event_id: str):
    return db.query(NBAEvent).filter(NBAEvent.event_id == event_id).first()


def create_NBAplayer(db: Session, player_data: dict, player_stats: dict):
    try:
        player_id = str(player_data.get('player_id'))
        existing_player = db.query(NBAPlayer).filter_by(player_id=player_id).first()
        
        if existing_player: 
            return existing_player
        
        player = NBAPlayer()

        for field in [
            "name", "team_name", "position", "height", "weight", "birth_date",
            "school", "country", "jersey_number", "from_year", "to_year",
            "draft_year", "draft_round", "draft_number"
        ]:
            if field in player_data:
                setattr(player, field, player_data.get(field))

        for stat_field in ["points", "rebounds", "assists"]:
            if stat_field in player_stats:
                setattr(player, stat_field, player_stats.get(stat_field))

        db.add(player)
        db.commit()
        db.refresh(player)
        print(f"{player.name} added to database")
        return player

    except IntegrityError:
        db.rollback()
        print(f"⚠️ Integrity error for player ID {player_data.get('player_id')}")
        return None
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting player ID {player_data.get('player_id')}: {e}")
        return None
    
def update_NBAplayer(db: Session, player_data: dict, player_stats: dict):
    try:
        player_id = str(player_data.get('player_id'))
        existing_player = db.query(NBAPlayer).filter_by(player_id=player_id).first()

        for field in [
                "team_name", "position", "height", "weight",
                "country", "jersey_number", "to_year",
            ]:
                if field in player_data:
                    setattr(existing_player, field, player_data.get(field))
            
        for stat_field in ["points", "rebounds", "assists"]:
            if stat_field in player_stats:
                setattr(existing_player, stat_field, player_stats.get(stat_field))

        db.commit()
        db.refresh(existing_player)
        print(f"{existing_player.name} UPDATED INFO")
        return existing_player 

    except IntegrityError:
        db.rollback()
        print(f"⚠️ Integrity error for player ID {player_data.get('player_id')}")
        return None
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating player ID {player_data.get('player_id')}: {e}")
        return None



def get_NBAplayer_by_id(db: Session, player_id: str):
    return db.query(NBAPlayer).filter(NBAPlayer.player_id == str(player_id)).first()


def create_NBAteam_odds(db: Session, odds_data: dict, event_id: int):
    market_types = ["moneyline", "spread", "total"]
    created_odds = []
    
    for market_type in market_types:
        if market_type in odds_data.get("markets", {}):
            try:
                transformed_data = transform_odds_data(odds_data, market_type)
                
                existing_team_odds = db.query(NBATeamOdds).filter_by(
                    event_id=event_id,
                    bookmaker=transformed_data["bookmaker"],
                    odds_type=transformed_data["odds_type"]
                ).first()

                if existing_team_odds:
                    for key, value in transformed_data.items():
                        if value is not None:
                            setattr(existing_team_odds, key, value)
                    db.commit()
                    db.refresh(existing_team_odds)
                    created_odds.append(existing_team_odds)
                    continue
                
                odds = NBATeamOdds(
                    event_id=event_id,
                    **transformed_data
                )
                db.add(odds)
                db.commit()
                db.refresh(odds)
                created_odds.append(odds)
            except Exception as e:
                db.rollback()
                raise e
    
    return created_odds


def get_NBAteam_odds_by_event_id(db: Session, event_id: int):
    return db.query(NBATeamOdds).filter(NBATeamOdds.event_id == event_id).all()


def create_NBAplayer_props(db: Session, props_data: dict, player_id: int, event_id: int):
    try:
        transformed_data = transform_prop_data(props_data)
        
        existing_props = db.query(NBAPlayerProps).filter_by(
            player_id=player_id, 
            event_id=event_id, 
            prop_type=transformed_data["prop_type"],
            bookmaker=transformed_data["bookmaker"]
        ).first()

        if existing_props:
            for key, value in transformed_data.items():
                setattr(existing_props, key, value)
            db.commit()
            db.refresh(existing_props)
            return existing_props
        
        props = NBAPlayerProps(
            player_id=player_id,
            event_id=event_id,
            **transformed_data
        )
        db.add(props)
        db.commit()
        db.refresh(props)
        return props
    except IntegrityError:
        db.rollback()
        return db.query(NBAPlayerProps).filter_by(
            player_id=player_id,
            event_id=event_id,
            prop_type=transformed_data["prop_type"],
            bookmaker=transformed_data["bookmaker"]
        ).first()
    except Exception as e:
        db.rollback()
        raise e


def get_NBAplayer_props_by_player_id(db: Session, player_id: int):
    return db.query(NBAPlayerProps).filter(NBAPlayerProps.player_id == player_id).all()


def create_player_gamelog(db: Session, gamelog_data: dict):
    try:
        transformed_data = transform_gamelog_data(gamelog_data)
        
        player = get_NBAplayer_by_id(db, transformed_data["player_id"])
        if not player:
            raise ValueError(f"Player with ID {transformed_data['player_id']} not found in database")

        existing_log = db.query(NBAPlayerGamelogs).filter_by(
            player_id=player.id,
            game_id=transformed_data["game_id"]
        ).first()

        if existing_log:
            return existing_log

        event_id = None

        # Remove 'player_id' from transformed_data to avoid duplication
        transformed_data.pop("player_id", None)

        log = NBAPlayerGamelogs(
            player_id=player.id,
            event_id=event_id,
            **transformed_data
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    except IntegrityError:
        db.rollback()
        player = get_NBAplayer_by_id(db, transformed_data["player_id"])
        return db.query(NBAPlayerGamelogs).filter_by(
            player_id=player.id if player else None,
            game_id=transformed_data["game_id"]
        ).first()
    except Exception as e:
        db.rollback()
        raise e



def get_NBAplayer_gamelog(db: Session, player_id: str, game_id: str):
    player = get_NBAplayer_by_id(db, player_id)
    if not player:
        return None
    
    return db.query(NBAPlayerGamelogs).filter(
        NBAPlayerGamelogs.player_id == player.id,
        NBAPlayerGamelogs.game_id == game_id
    ).first()


