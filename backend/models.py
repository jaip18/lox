from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(String, unique=True, index=True) 
    name = Column(String)
    sport = Column(String)

    events = relationship("NBAEvent", back_populates="league")


class NBAEvent(Base):
    __tablename__ = "NBA_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)  
    league_id = Column(Integer, ForeignKey("leagues.id"))
    home_team = Column(String)
    away_team = Column(String)
    start_time = Column(DateTime)
    status = Column(String, nullable=True)  

    league = relationship("League", back_populates="events")
    team_odds = relationship("NBATeamOdds", back_populates="event")
    player_props = relationship("NBAPlayerProps", back_populates="event")
    player_gamelogs = relationship("NBAPlayerGamelogs", back_populates="event")


class NBAPlayer(Base):
    __tablename__ = "NBA_players"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, unique=True, index=True)  
    name = Column(String)
    team_name = Column(String)
    position = Column(String)
    height = Column(String)
    weight = Column(String)
    birth_date = Column(String)  
    school = Column(String)
    country = Column(String)
    jersey_number = Column(String)
    from_year = Column(String, nullable=True)  
    to_year = Column(String, nullable=True)  
    draft_year = Column(String, nullable=True)  
    draft_round = Column(String, nullable=True)  
    draft_number = Column(String, nullable=True)  

    points = Column(Float, nullable=True)
    rebounds = Column(Float, nullable=True)
    assists = Column(Float, nullable=True)

    props = relationship("NBAPlayerProps", back_populates="player")
    gamelogs = relationship("NBAPlayerGamelogs", back_populates="player")


class NBATeamOdds(Base):   
    __tablename__ = "NBA_team_odds"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("NBA_events.id"))
    bookmaker = Column(String)
    odds_type = Column(String)  
    home_odds = Column(Float, nullable=True)
    away_odds = Column(Float, nullable=True)
    prop_odds = Column(Float, nullable=True)
    spread = Column(Float, nullable=True)
    total = Column(Float, nullable=True)
    last_update = Column(DateTime, nullable=True)  

    event = relationship("NBAEvent", back_populates="team_odds")


class NBAPlayerProps(Base):
    __tablename__ = "NBA_player_props"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("NBA_players.id"))
    event_id = Column(Integer, ForeignKey("NBA_events.id"))
    bookmaker = Column(String)
    prop_type = Column(String)  
    over_odds = Column(Float)
    under_odds = Column(Float)
    line = Column(Float)
    last_update = Column(DateTime, nullable=True)  

    player = relationship("NBAPlayer", back_populates="props")
    event = relationship("NBAEvent", back_populates="player_props")


class NBAPlayerGamelogs(Base):
    __tablename__ = "NBA_player_gamelogs"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("NBA_players.id"))
    game_id = Column(String)  
    event_id = Column(Integer, ForeignKey("NBA_events.id"), nullable=True)  
    game_date = Column(String)  

    minutes = Column(Integer, nullable=True)
    field_goals_made = Column(Integer, nullable=True)
    field_goal_attempts = Column(Integer, nullable=True)
    field_goal_percent = Column(Float, nullable=True) 
    three_pt_made = Column(Integer, nullable=True)
    three_pt_attempts = Column(Integer, nullable=True)
    three_pt_percent = Column(Float, nullable=True)
    free_throw_made = Column(Integer, nullable=True)
    free_throw_attempts = Column(Integer, nullable=True)
    free_throw_percent = Column(Float, nullable=True)
    offensive_rebound = Column(Integer, nullable=True)
    defensive_rebound = Column(Integer, nullable=True)
    rebounds = Column(Integer, nullable=True)
    assists = Column(Integer, nullable=True)
    steals = Column(Integer, nullable=True)
    blocks = Column(Integer, nullable=True)
    turnovers = Column(Integer, nullable=True)
    personal_fouls = Column(Integer, nullable=True)
    points = Column(Integer, nullable=True)
    plus_minus = Column(Float, nullable=True)  

    player = relationship("NBAPlayer", back_populates="gamelogs")
    event = relationship("NBAEvent", back_populates="player_gamelogs")



